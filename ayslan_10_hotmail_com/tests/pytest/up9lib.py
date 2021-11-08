"""
Helper functions of UP9
"""
import _thread
import base64
import codecs
import io
import json
import json as json_lib
import logging
import os
import random
import re
import struct
import sys
import threading
import time
import unittest
import uuid
import warnings
from collections import abc
from contextlib import contextmanager
from functools import wraps
from http.cookiejar import parse_ns_headers, Cookie  # noqa
from urllib import parse as urllib_parse
from urllib.parse import urlencode, unquote

import ddt
import requests
from jsonpath_ng.ext import parse as jsonpath_parse
from jsonpath_ng.jsonpath import DatumInContext, Fields
from lxml import html
from requests.cookies import merge_cookies, cookiejar_from_dict
from requests.structures import CaseInsensitiveDict
from urllib3.exceptions import InsecureRequestWarning

import apiritif
from apiritif import http, recorder
from apiritif.http import HTTPTarget, HTTPResponse

# the below block is just to avoid "unused import" in IDE

assert unittest
assert http
assert urlencode
assert uuid
assert unquote

warnings.simplefilter("ignore", InsecureRequestWarning)  # genson somehow avoids catching those in specific place

TAKE_RANDOM = os.environ.get("UP9_RANDOMIZE_EXTRACTS", False)


class _FSBacked(dict):  # this class allows saving RAM on large traces
    def __init__(self, fname) -> None:
        super().__init__()
        self.fname = fname
        logging.debug("Using FS map for trace: %s", self.fname)
        self.fd = open(self.fname, 'w')
        self.cnt = 0

    def __del__(self):
        if not self.fd.closed:
            self.fd.close()
        os.remove(self.fname)

    def __setitem__(self, k, v) -> None:
        logging.debug("Begin writing FS-backed entry for dict key %r", k)
        self.fd.write(json.dumps([k, v]) + "\n")
        self.cnt += 1
        logging.debug("Done FS-backed entry for dict key %r", k)

    def __len__(self) -> int:
        return self.cnt

    def items(self):
        if not self.fd.closed:
            self.fd.close()

        with open(self.fname) as fp:
            for line in fp:
                data = json.loads(line)
                yield data[0], data[1]

        self.__del__()


try:
    import pytest
    from apiritif.pytest_plugin import ApiritifPytestPlugin

    if pytest.mark._config:
        aplugin = pytest.mark._config.pluginmanager.getplugin(ApiritifPytestPlugin.__name__)
        if aplugin:
            aplugin._trace_map = _FSBacked(aplugin._result_file + '.map.tmp')
except ImportError:
    logging.debug("Did not register pytest changes")


class Context(object):
    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()
        self.targets = {}
        self.global_headers = {}
        self.grpc_mapping = {}

    def clear(self):
        self.session = requests.Session()
        self.targets.clear()
        self.global_headers.clear()
        self.grpc_mapping.clear()


_context = Context()


def extractor_decorator(a_method):
    @wraps(a_method)
    def _impl(*method_args, **method_kwargs):
        method_name = getattr(a_method, '__name__')
        extras = {
            "args": list(method_args)[:-1],
            "kwargs": method_kwargs,
            "failed": False,
            "value": None,
        }
        if method_args and isinstance(method_args[-1], HTTPResponse):
            evt = GenericEvent("extract", method_name, method_args[-1], extras)
            try:
                evt.extras['value'] = a_method(*method_args, **method_kwargs)
                return evt.extras['value']
            except BaseException:
                evt.extras['failed'] = True
                raise
            finally:
                recorder.record_event(evt)
        else:
            return a_method(*method_args, **method_kwargs)

    return _impl


@extractor_decorator
def get_data_from_header(spec, resp=None):
    header_dict = CaseInsensitiveDict()
    header_dict.update(_context.global_headers)
    if resp:
        header_dict.update(resp.headers)
    return header_dict.get(spec, "")


@extractor_decorator
def get_data_from_cookie(spec):
    c_dict = _context.session.cookies.get_dict()
    if spec not in c_dict:
        raise KeyError("Failed to find cookie %r" % spec)
    return c_dict[spec]


def get_first_row_from_dataset(file_name):
    with open(file_name) as dtst_file:
        dataset = json.load(dtst_file)
    row = dataset['rows'][0]
    return tuple(row[x['name']] for x in dataset['parameters'])


_JP_CACHE = {}


def jsonpath_field_update_monkey_patch(self, data, val):
    """
    Used as a monkey patch for jsonpath_ng.jsonpath.Fields.update
    to update only scalar fields with scalar values
    """
    if data is not None:
        for field in self.reified_fields(DatumInContext.wrap(data)):
            if field in data \
               and (isinstance(data[field], str) or not
                    isinstance(data[field], (abc.Sequence, abc.Mapping))) \
               and (isinstance(val, str) or not
                    isinstance(val, (abc.Sequence, abc.Mapping))):
                if hasattr(val, '__call__'):
                    val(data[field], data, field)
                else:
                    data[field] = val
    return data


Fields.update = jsonpath_field_update_monkey_patch


def apply_into_json(data, jpath, val):
    if jpath not in _JP_CACHE:
        _JP_CACHE[jpath] = jsonpath_parse(jpath)
    _JP_CACHE[jpath].update(data, val)


@extractor_decorator
def jsonpath(path, resp):
    if isinstance(resp, bytes):
        resp = resp.decode('utf-8')

    if isinstance(resp, str):
        data = json.loads(resp)
    else:
        data = resp.json()

    expr = jsonpath_parse(path)
    vals = [x.value for x in expr.find(data)]
    if vals:
        return random.choice(vals) if TAKE_RANDOM else vals[0]
    else:
        raise KeyError("jsonpath: No values found for %r" % path)


@extractor_decorator
def from_regex(regexp, text):
    pat = re.compile(regexp)
    vals = pat.findall(text)
    if vals:
        return random.choice(vals) if TAKE_RANDOM else vals[0]
    else:
        raise KeyError("regexp: No values found for %r" % regexp)


@extractor_decorator
def cssselect(sel, resp):
    if isinstance(resp, str):
        data = resp
    else:
        data = resp.text

    parts = sel.split(' ')
    if parts[-1].startswith('@'):
        attr = parts[-1][1:]
        parts.pop()
        sel = ' '.join(parts)
    else:
        attr = None

    tree = html.fromstring(data)
    q = tree.cssselect(sel)
    vals = [x.text if attr is None else x.attrib[attr] for x in q]
    if vals:
        result = random.choice(vals) if TAKE_RANDOM else vals[0]
        return result.strip()
    else:
        raise KeyError("cssselect: No values found for %r" % sel)


@extractor_decorator
def url_part(ospec, url):
    logging.debug("Extracting %r from %r", ospec, url)
    flag = ospec[0]
    spec = ospec[1:]

    parse_link = urllib_parse.urlparse(url)
    if flag == '/':
        ind = int(spec)
        path_parts = parse_link.path.split('/')
        if len(path_parts) - 1 <= ind:
            raise IndexError("No path element #%s in %r, failed extract" % (ind, parse_link.path))
        return path_parts[ind]
    elif flag == '#':
        get_part = urllib_parse.parse_qs(parse_link.fragment)
    else:
        get_part = urllib_parse.parse_qs(parse_link.query)

    if spec not in get_part:
        raise KeyError("Failed to find element %r inside URL: %s" % (spec, url))
    vals = get_part[spec]
    return random.choice(vals) if TAKE_RANDOM else vals[0]


def random_first_name():
    names = ('John', 'Peter', 'Bob', 'David', 'Harry')
    return random.choice(names)


def random_last_name():
    surnames = ('Black', 'Clark', 'Duncan', 'Gibson', 'James')
    return random.choice(surnames)


def random_email(domain=None):
    names = ('John', 'Peter', 'Bob', 'David', 'Harry')
    surnames = ('Black', 'Clark', 'Duncan', 'Gibson', 'James')
    email_domains = ('gmail.com', 'yahoo.com', 'hotmail.com')

    username = f'{random.choice(names)}.{random.choice(surnames)}'.lower()
    email = f'{username}@%s' % domain if domain else random.choice(email_domains)
    return email


def clear_session(metadata):
    def decorator(orig_fn):
        def wrapper(*args, **kwargs):
            metadata.update({
                'module': orig_fn.__module__, 'functionName': orig_fn.__qualname__
            })
            _do_clear_session(metadata)

            try:
                return orig_fn(*args, **kwargs)
            finally:
                logging.debug("Finished context: %s", metadata)

        return wrapper

    return decorator


def _do_clear_session(metadata):
    with apiritif.transaction("clear_session: " + json.dumps(metadata)):
        _context.clear()


def dummy_auth(tgt_key, target):
    # a callback to use when auth is suppressed
    # signature should match to authenticate()
    pass


def get_http_client(key, auth_callback=dummy_auth):
    if key in _context.targets:
        return _context.targets[key]

    target = TargetService(key)
    target.additional_headers({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 "
                                             "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"})
    target.additional_headers({"Referer": target.address + "/"})
    target.additional_headers({"Accept": "*/*"})
    _context.targets[key] = target

    with apiritif.transaction("authentication"):
        auth_callback(key, target)

    target.uses_auth = auth_callback is not dummy_auth

    _context.global_headers.update(target.get_additional_headers())
    if target.uses_auth:  # to support from_cookie() before any request happened
        target._headers_from_token_map({}, "", "")
    return target


# make the previous signature of `get_http_client` available for backwards compatibility
get_http_target = get_http_client


def _address_for_key(base_addr):
    if "://" in base_addr:
        tgt_key = target_key(base_addr)
    else:
        tgt_key = base_addr

    address = os.getenv(tgt_key, None)
    if address is not None:
        return address

    fname = "target_services.json"
    if not os.path.exists(fname):
        fname = os.path.join("data", fname)

    if os.path.exists(fname):
        with open(fname) as fp:
            mapping = json.load(fp)

        if base_addr in mapping:
            return mapping[base_addr]

        if tgt_key in mapping:
            return mapping[tgt_key]

    logging.debug("Service %r is not found in target URL mapping" % base_addr)
    return base_addr


def target_key(target_label):
    clean = lambda vstr: re.sub(r'\W|^(?=\d)', '_', vstr)

    parsed_uri = urllib_parse.urlparse(target_label)
    target_name = clean(parsed_uri.netloc)
    target_name = clean(target_label) if not target_name else target_name
    return 'TARGET_' + target_name.upper()


class TargetService(HTTPTarget):
    def __init__(self, target_key, base_path=None, use_cookies=True, additional_headers=None, keep_alive=True,
                 auto_assert_ok=False, timeout=60, allow_redirects=False):
        self.config_url = target_key
        self.access_key = None

        address = _address_for_key(target_key)

        timeout = float(os.getenv("UP9_HTTP_TIMEOUT", str(timeout)))
        super().__init__(address, base_path, use_cookies, additional_headers, keep_alive, auto_assert_ok, timeout,
                         allow_redirects, _context.session)

        self.auth_config = json.loads(os.getenv("UP9_AUTH_HEADERS_CONFIG", "{}"))
        self.config_url = target_key
        self.access_key = None
        self.address = address
        self.additional_headers({"x-abuse-info": "UP9.com generated tests"})
        self.grpc_stub = None
        self.uses_auth = False

    def request(self, method, path,
                params=None, headers=None, cookies=None, data=None, json=None, files=None,
                allow_redirects=None, timeout=None):

        if self.uses_auth:
            headers = self._headers_from_token_map(headers, method, path)
        else:
            logging.debug("Not using global auth headers for this call")

        overall_to = timeout if timeout is not None else self._timeout
        logging.debug("Entering timeout context")
        with timeout_scope(overall_to * 1.1 if overall_to is not None else None):  # prevent hang on slow or large dwnl
            resp = super().request(method, path, params, headers, cookies, data, json, files, allow_redirects, timeout)
        logging.debug("Left timeout context")

        if resp.headers.get('content-type', '').startswith('text/html'):
            self.additional_headers({"Referer": resp.url})
        return resp

    def _headers_update(self, payloads: dict, result: dict, item: dict):
        payload = item.get('payloadId', False)
        if payload is None:
            result.clear()
        elif payload:
            hdrs = payloads[payload]['headers']
            if hdrs:
                logging.debug("Setting headers from auth context: %s", hdrs)
                result.update(hdrs)

    def _headers_from_token_map(self, headers, method, path):
        if not len(_context.session.cookies):
            if isinstance(self.auth_config, dict) and 'cookies' in self.auth_config:
                merge_cookies_into_session(self.auth_config['cookies'])

        result = {}
        payloads = self.auth_config.get('entityPayloads', {})
        self._headers_update(payloads, result, self.auth_config)  # global level

        if self.config_url in self.auth_config.get('services', {}):  # service level
            svc = self.auth_config['services'][self.config_url]
            self._headers_update(payloads, result, svc)
            for item in svc.get('endpoints', []):  # request level
                same_method = item['method'].lower() == method.lower()
                patt = re.sub(r'{[^}]+}', '[^/]+', item['path'])
                same_path = re.match(patt, path)
                if same_method and same_path:
                    self._headers_update(payloads, result, item)

        result.update(headers if headers else {})
        return result if result else headers

    def get_additional_headers(self):
        return self._additional_headers

    def set_grpc(self, stub_class):
        parsed = urllib_parse.urlparse(self.address)
        if parsed.scheme == 'https':
            creds = grpc.ssl_channel_credentials()  # TODO: how to accept all certificates?
            channel = grpc.secure_channel(parsed.netloc if ':' in parsed.netloc else parsed.netloc + ':443', creds)
        else:
            channel = grpc.insecure_channel(parsed.netloc if ':' in parsed.netloc else parsed.netloc + ':80')

        intercepted = grpc.intercept_channel(channel, LoggingInterceptorUU(parsed.netloc, self._timeout))
        self.grpc_stub = stub_class(intercepted)


try:
    import grpc
    from grpc import UnaryUnaryClientInterceptor
    from grpc._interceptor import _ClientCallDetails

    class LoggingInterceptorUU(UnaryUnaryClientInterceptor):
        def __init__(self, address, timeout) -> None:
            super().__init__()
            self.address = address
            self.timeout = timeout

        def _into_b64(self, msg):
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
            data = str(base64.b64encode(msg.SerializeToString()), 'ascii')
            return "data:%s;base64,%s" % ('application/protobuf', data)

        def intercept_unary_unary(self, continuation, client_call_details: _ClientCallDetails, request):
            # inject timeout
            client_call_details = _ClientCallDetails(client_call_details.method, self.timeout,
                                                     client_call_details.metadata, client_call_details.credentials,
                                                     client_call_details.wait_for_ready,
                                                     client_call_details.compression)
            logging.info("Sending gRPC call to %r: %r", client_call_details.method, request)
            # FIXME: we work with continuation wrong here, should not been calling result() on it maybe?
            url = "grpc://" + self.address + client_call_details.method
            with apiritif.transaction(url) as tran:
                wrapped_req = self._make_request(client_call_details.method, url, request)
                tran.set_request(repr(request))
                tran.attach_extra("grpc_req_class", request.DESCRIPTOR.full_name)

                continuation = continuation(client_call_details, request)

                code = continuation.code()
                tran.set_response_code(code.value[0])
                msg = "gRPC status %s: %s" % (code, continuation.details())
                logging.info(msg)
                if code != grpc.StatusCode.OK:
                    tran.fail(msg)

                resp = continuation.result()
                tran.attach_extra("grpc_resp_class", resp.DESCRIPTOR.full_name)
                tran.set_response(repr(resp))
                logging.info("gRPC response: %r", resp)
                wrapped_response = self._make_response(resp, wrapped_req, code)
                recorder.record_http_request(client_call_details.method, self.address, wrapped_req, wrapped_response,
                                             _context.session)

                return continuation

        def _make_request(self, method, url, request):
            req = requests.Request(method, url=url, data=self._into_b64(request))
            prepared = req.prepare()
            _context.grpc_mapping[id(request)] = prepared
            return prepared

        def _make_response(self, resp_msg, wrapped_req, status):
            resp = requests.Response()
            resp.status_code = 200 if not status.value[0] else status.value[0]
            resp.request = wrapped_req
            resp._request = wrapped_req
            resp.msg = resp_msg
            resp.raw = io.BytesIO(self._into_b64(resp_msg).encode('utf8'))
            _context.grpc_mapping[id(resp_msg)] = resp
            return resp

    def wrap_grpc_for_tracing(resp):
        return _context.grpc_mapping[id(resp)]

except ImportError:
    logging.info("gRPC is not available")

_JSON_METADATA_ATTR = "%json_metadata_file_path"


def data_driven_tests(cls):
    ddt.ddt(cls)
    for name, func in list(cls.__dict__.items()):
        if hasattr(func, _JSON_METADATA_ATTR):
            file_attr = getattr(func, _JSON_METADATA_ATTR)

            with codecs.open(file_attr, 'r', 'utf-8') as f:
                data = json.load(f)

            _add_tests_from_data(cls, name, func, data)
            delattr(cls, name)  # removes original test method
    return cls


def json_dataset(value):
    def wrapper(func):
        setattr(func, _JSON_METADATA_ATTR, value)
        return func

    return wrapper


def _add_tests_from_data(cls, name, func, data):
    index_len = len(str(len(data['rows'])))
    for i, row in enumerate(data['rows']):
        value = tuple(row[x['name']] for x in data['parameters'])
        index = "{0:0{1}}".format(i + 1, index_len)
        test_name = "{0}_{1}".format(name, index)
        ddt.add_test(cls, test_name, test_name, func, value)
        if i >= int(os.getenv('UP9_LIMIT_DATASET', sys.maxsize)):
            logging.info("Interrupting dataset because of limit")
            break


def merge_cookies_into_session(cookies_input):
    jar = _context.session.cookies
    if isinstance(cookies_input, list):
        for item in cookies_input:
            cookie = Cookie(
                0, item['name'], item['value'], None, False, item['domain'], True,
                bool(item['domain'].startswith(".")), item['path'], True, item['secure'], None, False, "",
                "", {},
            )
            logging.debug("Set cookie into context: %r", cookie)
            jar.set_cookie(cookie)
    else:
        attrs_set = parse_ns_headers(cookies_input.split('; '))
        merge_cookies(jar, cookiejar_from_dict({x[0][0]: x[0][1] for x in attrs_set}))


class _Timeout(threading.Thread):
    def __init__(self, timeout):
        super().__init__(daemon=True)
        self.timeout = timeout
        self.canceled = False
        self.msg = None

    def run(self) -> None:
        if self.timeout is None:
            return

        logging.debug("Start tracking timeout in thread %r", id(self.ident))
        start = time.time()
        passed = 0
        while not self.canceled and passed < self.timeout:
            passed = time.time() - start
            remaining = self.timeout - passed
            if remaining > 1:
                logging.debug("Sleeping 1s in thread %s", id(self.ident))
                time.sleep(1)
            elif remaining > 0:
                logging.debug("Sleeping rest of %s in thread %r", remaining, id(self.ident))
                time.sleep(remaining)
            else:
                logging.debug("Timeout exhausted in thread %r: %s", id(self.ident), self.timeout)

        if not self.canceled:
            self.msg = "Timeout of %.3fs has expired" % self.timeout
            _thread.interrupt_main()
        else:
            logging.debug("Canceled timeout in thread %r", id(self.ident))


@contextmanager
def timeout_scope(to):
    def wrapper():
        watcher = _Timeout(to)
        watcher.start()
        try:
            yield
        except KeyboardInterrupt:
            if watcher.msg:
                raise TimeoutError(watcher.msg)
            else:
                raise
        finally:
            watcher.canceled = True

    yield from wrapper()


def _protobuf_action(message, spec, action):
    for field_no in spec.split('.'):
        field_no = int(field_no)
        field = message.DESCRIPTOR.fields_by_number[field_no]
        if field.type == field.TYPE_MESSAGE:
            message = getattr(message, field.name)
            if field.label == field.LABEL_REPEATED:
                message = message.add()
            continue
        else:
            return action(message, field)
    else:
        raise KeyError("Failed to find field in protobuf: %s", spec)


def apply_into_protobuf(message, spec, value):
    def set_val(message, field):
        if field.label == field.LABEL_REPEATED:
            message = getattr(message, field.name)
            message.append(value)
        else:
            setattr(message, field.name, value)

    _protobuf_action(message, spec, set_val)


def grpc_frame(data):
    return b'\x00' + struct.pack(">I", len(data)) + data


def grpc_unframe(data):
    is_compressed = data[0]
    assert not is_compressed, "Compressed GRPC frames are not supported"
    size = struct.unpack(">I", data[1:5])[0]
    data = data[5:]

    if len(data) > size:
        logging.warning("More than one message in GRPC payload is not supported, taking first")
        data = data[:size]
    return data


@recorder.assertion_decorator
def assert_grpc(resp, spec, expected_value=None):
    def do_assert(message, field):
        val = getattr(message, field.name)
        if expected_value is not None and val != expected_value:
            msg = "GRPC field (%r) value %r didn't match expected value: %s" % (field.name, val, expected_value)
            raise AssertionError(msg)

    _protobuf_action(resp.msg, spec, do_assert)


@extractor_decorator
def from_grpc_fields(spec, resp):
    def do_extract(message, field):
        return getattr(message, field.name)

    return _protobuf_action(resp.msg, spec, do_extract)


class GenericEvent(apiritif.Event):
    def __init__(self, etype, name, response, data):
        super().__init__(response)
        self.type = etype
        self.name = name
        self.extras = data

    def to_dict(self):
        res = {
            "type": self.type,
            "name": self.name,
        }
        res.update(self.extras)
        return res


try:
    from confluent_kafka.cimpl import Consumer, KafkaException, Producer

    class Kafka(object):
        def __init__(self, target_key) -> None:
            super().__init__()
            self.address = _address_for_key(target_key)
            kafka_config = {
                'bootstrap.servers': self.address,
                'group.id': "up9-test-group",
                'enable.auto.commit': 'false'  # important for passive observing
            }
            if "ssl://" in self.address.lower():
                kafka_config['security.protocol'] = 'SSL'

            self.consumer = Consumer(kafka_config)
            self.producer = Producer(kafka_config)
            self.watching_topics = []

            self.consumer.list_topics(timeout=5)  # to check for connectivity

        def watch_topics(self, topics: list):

            def my_on_assign(consumer, partitions):
                logging.debug("On assign: %r", partitions)
                consumer.assign(partitions)
                for partition in partitions:
                    low, high = consumer.get_watermark_offsets(partition)
                    partition.offset = high
                    logging.debug("Setting offset: %r", partition)
                    consumer.seek(partition)

            self.watching_topics.extend(topics)
            self.consumer.subscribe(topics, on_assign=my_on_assign)
            self.consumer.poll(0.01)  # to trigger partition assignments

        def get_watched_messages(self, interval=0.0, predicate=lambda x: True):
            logging.debug("Checking messages that appeared on kafka topics: %r", self.watching_topics)
            res = []

            start = time.time()
            while True:
                msg = self.consumer.poll(interval)
                if msg is None or time.time() - start > interval:
                    break  # done reading

                if msg.error():
                    raise KafkaException("kafka consumer error: {}".format(msg.error()))

                logging.debug("Potential message: %r", (msg.partition(), msg.key(), msg.headers(), msg.value()))
                if predicate(msg):
                    res.append(msg)

            # TODO: consumer.close()
            return res

        def assert_seen_message(self, resp, delay=0, predicate=lambda x: True):
            @recorder.assertion_decorator
            def assert_seen_kafka_message(resp, topics, delay):
                messages = self.get_watched_messages(delay, predicate)
                messages = [(m.topic(), m.key(), m.value(), m.headers()) for m in messages]
                if not messages:
                    raise AssertionError("No messages on Kafka topic %r" % topics)
                else:
                    logging.info("Validated the messages have appeared: %s", messages)

                return messages

            return assert_seen_kafka_message(resp, self.watching_topics, delay)

        def put(self, topic, data=None, json=None, headers=None):
            # TODO: parse key out of URL
            if topic.startswith('/'):
                topic = topic[1:]

            if data is None and json is not None:
                data = json_lib.dumps(json)

            with apiritif.transaction('kafka://[' + self.address + ']/' + topic):
                logging.info("Sending message to Kafka topic %r: %r", topic, data)
                self.producer.produce(topic, data, headers=[] if headers is None else headers)
                self.producer.poll(0)
                self.producer.flush()

                wrapped_req = self._make_request('PUT', 'kafka://' + self.address.split(',')[0] + '/' + topic, data)
                wrapped_response = self._make_response(wrapped_req)
                recorder.record_http_request('PUT', self.address, wrapped_req, wrapped_response, _context.session)

            return wrapped_response

        def _make_request(self, method, url, request):
            req = requests.Request(method, url=url, data=request)
            prepared = req.prepare()
            _context.grpc_mapping[id(request)] = prepared
            return prepared

        def _make_response(self, wrapped_req):
            resp = requests.Response()
            resp.status_code = 202
            resp.request = wrapped_req
            resp._request = wrapped_req
            resp.msg = 'Accepted'
            resp.raw = io.BytesIO()
            return resp
except ImportError:
    logging.info("confluent_kafka is not available")
