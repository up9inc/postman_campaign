from up9lib import *
from authentication import authenticate

# logging.basicConfig(level=logging.DEBUG)


@data_driven_tests
class Tests_www_airbnb_com_br(unittest.TestCase):

    @json_dataset('data/4/dataset_4.json')
    @clear_session({'spanId': 4})
    def test_04_post_param1_param2_9GA_param3_ATJQAQ_WBp_param4(self, data_row):
        device_memory, ect, param, param1, param2, param3, sensor_data, viewport_width = data_row

        # POST https://www.airbnb.com.br/{param1}/{param2}/9GA/{param3}/ATJQAQ/WBp/{param4} (endp 4)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        with open('data/4/payload_for_endp_4.json', 'r') as json_payload_file:
            json_payload = json.load(json_payload_file)
        apply_into_json(json_payload, '$.sensor_data', sensor_data)
        resp = www_airbnb_com_br.post(f'/{param}/{param1}/9GA/{param2}/ATJQAQ/WBp/{param3}', json=json_payload, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width})
        resp.assert_ok()
        # resp.assert_status_code(201)
        # self.assertLess(resp.elapsed.total_seconds(), 0.347)

    @json_dataset('data/5/dataset_5.json')
    @clear_session({'spanId': 5})
    def test_05_get_api_v2_autosuggestions(self, data_row):
        currency, device_memory, ect, key, options, viewport_width = data_row

        # GET https://www.airbnb.com.br/api/v2/autosuggestions (endp 5)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'currency': currency, 'key': key, 'locale': 'pt', 'options': options, 'refinement_paths[]': '/homes'})
        resp = www_airbnb_com_br.get('/api/v2/autosuggestions' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.experiment_data.control_metadata.name', expected_value='control')
        # self.assertLess(resp.elapsed.total_seconds(), 0.383)

    @json_dataset('data/6/dataset_6.json')
    @clear_session({'spanId': 6})
    def test_06_post_api_v2_client_configs(self, data_row):
        currency, device_memory, ect, key, userAttributes, viewport_width, x_csrf_token = data_row

        # POST https://www.airbnb.com.br/api/v2/client_configs (endp 6)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'currency': currency, 'key': key, 'locale': 'pt'})
        with open('data/6/payload_for_endp_6.json', 'r') as json_payload_file:
            json_payload = json.load(json_payload_file)
        apply_into_json(json_payload, '$.userAttributes[*]', userAttributes)
        resp = www_airbnb_com_br.post('/api/v2/client_configs' + qstr, json=json_payload, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-requested-with': 'XMLHttpRequest'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # self.assertLess(resp.elapsed.total_seconds(), 0.273)

    @json_dataset('data/7/dataset_7.json')
    @clear_session({'spanId': 7})
    def test_07_get_api_v2_host_referral_eligibilities(self, data_row):
        currency, device_memory, ect, key, touch_point, viewport_width, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v2/host_referral_eligibilities (endp 7)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'currency': currency, 'key': key, 'locale': 'pt', 'touch_point': touch_point})
        resp = www_airbnb_com_br.get('/api/v2/host_referral_eligibilities' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-requested-with': 'XMLHttpRequest'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # self.assertLess(resp.elapsed.total_seconds(), 0.212)

    @json_dataset('data/8/dataset_8.json')
    @clear_session({'spanId': 8})
    def test_08_post_api_v2_paid_growth_tracking_datas(self, data_row):
        _format, currency, device_memory, ect, key, listing_id, viewport_width, x_csrf_token = data_row

        # POST https://www.airbnb.com.br/api/v2/paid_growth_tracking_datas (endp 8)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_format': _format, 'currency': currency, 'key': key, 'locale': 'pt'})
        with open('data/8/payload_for_endp_8.json', 'r') as json_payload_file:
            json_payload = json.load(json_payload_file)
        apply_into_json(json_payload, '$.listing_id', listing_id)
        resp = www_airbnb_com_br.post('/api/v2/paid_growth_tracking_datas' + qstr, json=json_payload, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-requested-with': 'XMLHttpRequest'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.paid_growth_tracking_data.city', expected_value='Baependi')
        # self.assertLess(resp.elapsed.total_seconds(), 0.343)

    @json_dataset('data/9/dataset_9.json')
    @clear_session({'spanId': 9})
    def test_09_get_api_v2_paid_growth_tracking_datas(self, data_row):
        currency, device_memory, ect, key, viewport_width, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v2/paid_growth_tracking_datas (endp 9)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'currency': currency, 'key': key, 'locale': 'pt'})
        resp = www_airbnb_com_br.get('/api/v2/paid_growth_tracking_datas' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-requested-with': 'XMLHttpRequest'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.paid_growth_tracking_data[*].audience_type', expected_value='visitor')
        # self.assertLess(resp.elapsed.total_seconds(), 0.318)

    @json_dataset('data/10/dataset_10.json')
    @clear_session({'spanId': 10})
    def test_10_get_api_v2_user_markets(self, data_row):
        currency, device_memory, ect, key, viewport_width, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v2/user_markets (endp 10)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'currency': currency, 'key': key, 'language': 'pt', 'locale': 'pt'})
        resp = www_airbnb_com_br.get('/api/v2/user_markets' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-requested-with': 'XMLHttpRequest'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.user_markets[*].locale', expected_value='pt')
        # self.assertLess(resp.elapsed.total_seconds(), 0.329)

    @json_dataset('data/11/dataset_11.json')
    @clear_session({'spanId': 11})
    def test_11_get_api_v3_Header(self, data_row):
        _cb, currency, device_memory, ect, extensions, variables, viewport_width, x_airbnb_api_key, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v3/Header (endp 11)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_cb': _cb, 'currency': currency, 'extensions': extensions, 'locale': 'pt', 'operationName': 'Header', 'variables': variables})
        resp = www_airbnb_com_br.get('/api/v3/Header' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-airbnb-api-key': x_airbnb_api_key, 'x-airbnb-graphql-platform': 'web', 'x-airbnb-graphql-platform-client': 'minimalist-niobe', 'x-airbnb-supports-airlock-v2': 'true', 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-niobe-short-circuited': 'true'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.data.presentation.header.menuItemGroups[*].__typename', expected_value='HeaderItemGroup')
        # self.assertLess(resp.elapsed.total_seconds(), 0.246)

    @json_dataset('data/12/dataset_12.json')
    @clear_session({'spanId': 12})
    def test_12_get_api_v3_PdpAvailabilityCalendar(self, data_row):
        _cb, currency, device_memory, ect, extensions, variables, viewport_width, x_airbnb_api_key, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v3/PdpAvailabilityCalendar (endp 12)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_cb': _cb, 'currency': currency, 'extensions': extensions, 'locale': 'pt', 'operationName': 'PdpAvailabilityCalendar', 'variables': variables})
        resp = www_airbnb_com_br.get('/api/v3/PdpAvailabilityCalendar' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-airbnb-api-key': x_airbnb_api_key, 'x-airbnb-graphql-platform': 'web', 'x-airbnb-graphql-platform-client': 'minimalist-niobe', 'x-airbnb-supports-airlock-v2': 'true', 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-niobe-short-circuited': 'true'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.data.merlin.pdpAvailabilityCalendar.calendarMonths[*].__typename', expected_value='MerlinCalendarMonth')
        # self.assertLess(resp.elapsed.total_seconds(), 0.565)

    @json_dataset('data/13/dataset_13.json')
    @clear_session({'spanId': 13})
    def test_13_get_api_v3_PdpPhotoTour(self, data_row):
        _cb, currency, device_memory, ect, extensions, variables, viewport_width, x_airbnb_api_key, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v3/PdpPhotoTour (endp 13)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_cb': _cb, 'currency': currency, 'extensions': extensions, 'locale': 'pt', 'operationName': 'PdpPhotoTour', 'variables': variables})
        resp = www_airbnb_com_br.get('/api/v3/PdpPhotoTour' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-airbnb-api-key': x_airbnb_api_key, 'x-airbnb-graphql-platform': 'web', 'x-airbnb-graphql-platform-client': 'minimalist-niobe', 'x-airbnb-supports-airlock-v2': 'true', 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-niobe-short-circuited': 'true'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.data.merlin.pdpPhotoTour.saveButton.loggingEventData.section', expected_value='photoTour')
        # self.assertLess(resp.elapsed.total_seconds(), 0.460)

    @json_dataset('data/14/dataset_14.json')
    @clear_session({'spanId': 14})
    def test_14_get_api_v3_PdpReviews(self, data_row):
        _cb, currency, device_memory, ect, extensions, operationName, variables, viewport_width, x_airbnb_api_key, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v3/PdpReviews (endp 14)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_cb': _cb, 'currency': currency, 'extensions': extensions, 'locale': 'pt', 'operationName': operationName, 'variables': variables})
        resp = www_airbnb_com_br.get('/api/v3/PdpReviews' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-airbnb-api-key': x_airbnb_api_key, 'x-airbnb-graphql-platform': 'web', 'x-airbnb-graphql-platform-client': 'minimalist-niobe', 'x-airbnb-supports-airlock-v2': 'true', 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-niobe-short-circuited': 'true'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.data.merlin.__typename', expected_value='MerlinQuery')
        # self.assertLess(resp.elapsed.total_seconds(), 0.338)

    @json_dataset('data/15/dataset_15.json')
    @clear_session({'spanId': 15})
    def test_15_get_api_v3_SearchBlocksQuery(self, data_row):
        _cb, currency, device_memory, ect, extensions, variables, viewport_width, x_airbnb_api_key, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v3/SearchBlocksQuery (endp 15)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_cb': _cb, 'currency': currency, 'extensions': extensions, 'locale': 'pt', 'operationName': 'SearchBlocksQuery', 'variables': variables})
        resp = www_airbnb_com_br.get('/api/v3/SearchBlocksQuery' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-airbnb-api-key': x_airbnb_api_key, 'x-airbnb-graphql-platform': 'web', 'x-airbnb-graphql-platform-client': 'minimalist-niobe', 'x-airbnb-supports-airlock-v2': 'true', 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-niobe-short-circuited': 'true'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.data.dora.__typename', expected_value='DoraQuery')
        # self.assertLess(resp.elapsed.total_seconds(), 0.429)

    @json_dataset('data/16/dataset_16.json')
    @clear_session({'spanId': 16})
    def test_16_get_api_v3_StaysPdpSections(self, data_row):
        _cb, currency, device_memory, ect, extensions, variables, viewport_width, x_airbnb_api_key, x_csrf_token = data_row

        # GET https://www.airbnb.com.br/api/v3/StaysPdpSections (endp 16)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        qstr = '?' + urlencode({'_cb': _cb, 'currency': currency, 'extensions': extensions, 'locale': 'pt', 'operationName': 'StaysPdpSections', 'variables': variables})
        resp = www_airbnb_com_br.get('/api/v3/StaysPdpSections' + qstr, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width, 'x-airbnb-api-key': x_airbnb_api_key, 'x-airbnb-graphql-platform': 'web', 'x-airbnb-graphql-platform-client': 'minimalist-niobe', 'x-airbnb-supports-airlock-v2': 'true', 'x-csrf-token': x_csrf_token, 'x-csrf-without-token': '1', 'x-niobe-short-circuited': 'true'})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # resp.assert_jsonpath('$.data.presentation.stayProductDetailPage.sections.metadata.pdpType', expected_value='MARKETPLACE')
        # self.assertLess(resp.elapsed.total_seconds(), 0.418)

    @json_dataset('data/17/dataset_17.json')
    @clear_session({'spanId': 17})
    def test_17_post_tracking_airdog(self, data_row):
        device_memory, ect, metric, tags, viewport_width = data_row

        # POST https://www.airbnb.com.br/tracking/airdog (endp 17)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        with open('data/17/payload_for_endp_17.json', 'r') as json_payload_file:
            json_payload = json.load(json_payload_file)
        apply_into_json(json_payload, '$[*].metric', metric)
        apply_into_json(json_payload, '$[*].tags[*]', tags)
        resp = www_airbnb_com_br.post('/tracking/airdog', json=json_payload, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width})
        resp.assert_ok()
        # resp.assert_status_code(204)
        # self.assertLess(resp.elapsed.total_seconds(), 0.215)

    @json_dataset('data/18/dataset_18.json')
    @clear_session({'spanId': 18})
    def test_18_post_tracking_jitney_logging_messages(self, data_row):
        accuracy_rating, action, action_type, bev, cache_hit_ratio, canonical_host, canonical_url, checkin_rating, cleanliness_rating, client_session_id, client_version, communication_rating, component, count, count1, count2, count3, custom_data, decodedbody_size, decodedbody_size1, decodedbody_size2, decodedbody_size3, device_id, device_memory, device_year_class, document_age, domain_and_path, downlink, ect, effective_type, encodedbody_size, encodedbody_size1, encodedbody_size2, encodedbody_size3, event_data, event_data1, event_data2, event_data_schema, event_data_schema1, event_id, event_name, event_name1, experiment, external_stylesheet_rules, guest_satisfaction_overall, had_cached_data, hosting_id, http_method, http_status_code, impression_uuid, impression_uuid1, inline_stylesheet_rules, lcp, listing_id, listing_lat, listing_lng, location_rating, logging_id, longest_blocking_time, network_deserialization_latency_ms, operation, operation_id, operation_name, page, page_name, page_name1, page_referrer, page_uri, page_view_duration, picture_count, recorder_duration, referrer, remarketing_id, req_uuid, request_strategy, rtt, schema, schema1, screen_height, screen_width, subject_id, subject_type, tbt, total_view_duration, trackingjs_logging_version, transfer_size, transfer_size1, transfer_size2, transfer_size3, treatment, ttfcp, ttfmp, url, user_agent, user_bucket, utc_offset, uuid_, value_rating, version, viewport_width, visitor_id, visitor_id1, web_tab_uuid = data_row

        # POST https://www.airbnb.com.br/tracking/jitney/logging/messages (endp 18)
        www_airbnb_com_br = get_http_client('https://www.airbnb.com.br', authenticate)
        with open('data/18/payload_for_endp_18.json', 'r') as json_payload_file:
            json_payload = json.load(json_payload_file)
        apply_into_json(json_payload, '$[*].event_data.*', event_data)
        apply_into_json(json_payload, '$[*].event_data.accuracy_rating', accuracy_rating)
        apply_into_json(json_payload, '$[*].event_data.amenities[*]', int(random.randint(1, 510)))
        apply_into_json(json_payload, '$[*].event_data.app_logging_context.active_sessions[*].event_data', event_data1)
        apply_into_json(json_payload, '$[*].event_data.app_logging_context.active_sessions[*].event_data_schema', event_data_schema)
        apply_into_json(json_payload, '$[*].event_data.app_logging_context.active_sessions[*].uuid', uuid_)
        apply_into_json(json_payload, '$[*].event_data.app_logging_context.web_tab_uuid', web_tab_uuid)
        apply_into_json(json_payload, '$[*].event_data.assets.css.count', count)
        apply_into_json(json_payload, '$[*].event_data.assets.css.decodedbody_size', decodedbody_size)
        apply_into_json(json_payload, '$[*].event_data.assets.css.encodedbody_size', encodedbody_size)
        apply_into_json(json_payload, '$[*].event_data.assets.css.transfer_size', transfer_size)
        apply_into_json(json_payload, '$[*].event_data.assets.font.count', count1)
        apply_into_json(json_payload, '$[*].event_data.assets.font.decodedbody_size', decodedbody_size1)
        apply_into_json(json_payload, '$[*].event_data.assets.font.encodedbody_size', encodedbody_size1)
        apply_into_json(json_payload, '$[*].event_data.assets.font.transfer_size', transfer_size1)
        apply_into_json(json_payload, '$[*].event_data.assets.img.count', count2)
        apply_into_json(json_payload, '$[*].event_data.assets.img.decodedbody_size', decodedbody_size2)
        apply_into_json(json_payload, '$[*].event_data.assets.img.encodedbody_size', encodedbody_size2)
        apply_into_json(json_payload, '$[*].event_data.assets.img.transfer_size', transfer_size2)
        apply_into_json(json_payload, '$[*].event_data.assets.js.airbnb.cache_hit_ratio', cache_hit_ratio)
        apply_into_json(json_payload, '$[*].event_data.assets.js.airbnb.count', count3)
        apply_into_json(json_payload, '$[*].event_data.assets.js.airbnb.decodedbody_size', decodedbody_size3)
        apply_into_json(json_payload, '$[*].event_data.assets.js.airbnb.encodedbody_size', encodedbody_size3)
        apply_into_json(json_payload, '$[*].event_data.assets.js.airbnb.transfer_size', transfer_size3)
        apply_into_json(json_payload, '$[*].event_data.cache_response_byte_size', int(random.randint(758, 6921)))
        apply_into_json(json_payload, '$[*].event_data.checkin_rating', checkin_rating)
        apply_into_json(json_payload, '$[*].event_data.cleanliness_rating', cleanliness_rating)
        apply_into_json(json_payload, '$[*].event_data.client_version', client_version)
        apply_into_json(json_payload, '$[*].event_data.communication_rating', communication_rating)
        apply_into_json(json_payload, '$[*].event_data.component', component)
        apply_into_json(json_payload, '$[*].event_data.context.bev', bev)
        apply_into_json(json_payload, '$[*].event_data.context.client_session_id', client_session_id)
        apply_into_json(json_payload, '$[*].event_data.context.device.device_year_class', device_year_class)
        apply_into_json(json_payload, '$[*].event_data.context.impression_uuid', impression_uuid)
        apply_into_json(json_payload, '$[*].event_data.context.page_name', page_name)
        apply_into_json(json_payload, '$[*].event_data.context.screen_height', screen_height)
        apply_into_json(json_payload, '$[*].event_data.context.screen_width', screen_width)
        apply_into_json(json_payload, '$[*].event_data.context.timestamp', int(int(time.time() * 1000)))
        apply_into_json(json_payload, '$[*].event_data.context.user_agent', user_agent)
        apply_into_json(json_payload, '$[*].event_data.context.version', version)
        apply_into_json(json_payload, '$[*].event_data.context.visitor_id', visitor_id)
        apply_into_json(json_payload, '$[*].event_data.context.web.action', action)
        apply_into_json(json_payload, '$[*].event_data.context.web.canonical_host', canonical_host)
        apply_into_json(json_payload, '$[*].event_data.context.web.canonical_url', canonical_url)
        apply_into_json(json_payload, '$[*].event_data.context.web.page_referrer', page_referrer)
        apply_into_json(json_payload, '$[*].event_data.context.web.page_uri', page_uri)
        apply_into_json(json_payload, '$[*].event_data.context.web.req_uuid', req_uuid)
        apply_into_json(json_payload, '$[*].event_data.custom_data', custom_data)
        apply_into_json(json_payload, '$[*].event_data.device_id', device_id)
        apply_into_json(json_payload, '$[*].event_data.document_age', document_age)
        apply_into_json(json_payload, '$[*].event_data.domain_and_path', domain_and_path)
        apply_into_json(json_payload, '$[*].event_data.event_data', event_data2)
        apply_into_json(json_payload, '$[*].event_data.event_data_schema', event_data_schema1)
        apply_into_json(json_payload, '$[*].event_data.event_id', event_id)
        apply_into_json(json_payload, '$[*].event_data.event_name', event_name)
        apply_into_json(json_payload, '$[*].event_data.experiment', experiment)
        apply_into_json(json_payload, '$[*].event_data.external_stylesheet_rules', external_stylesheet_rules)
        apply_into_json(json_payload, '$[*].event_data.first_response_latency_ms', int(random.randint(0, 582)))
        apply_into_json(json_payload, '$[*].event_data.guest_satisfaction_overall', guest_satisfaction_overall)
        apply_into_json(json_payload, '$[*].event_data.had_cached_data', had_cached_data)
        apply_into_json(json_payload, '$[*].event_data.hosting_id', hosting_id)
        apply_into_json(json_payload, '$[*].event_data.http_method', http_method)
        apply_into_json(json_payload, '$[*].event_data.http_status_code', http_status_code)
        apply_into_json(json_payload, '$[*].event_data.impression_uuid', impression_uuid1)
        apply_into_json(json_payload, '$[*].event_data.inline_stylesheet_rules', inline_stylesheet_rules)
        apply_into_json(json_payload, '$[*].event_data.lcp', lcp)
        apply_into_json(json_payload, '$[*].event_data.listing_id', listing_id)
        apply_into_json(json_payload, '$[*].event_data.listing_lat', listing_lat)
        apply_into_json(json_payload, '$[*].event_data.listing_lng', listing_lng)
        apply_into_json(json_payload, '$[*].event_data.location_rating', location_rating)
        apply_into_json(json_payload, '$[*].event_data.logging_id', logging_id)
        apply_into_json(json_payload, '$[*].event_data.longest_blocking_time', longest_blocking_time)
        apply_into_json(json_payload, '$[*].event_data.network_deserialization_latency_ms', network_deserialization_latency_ms)
        apply_into_json(json_payload, '$[*].event_data.network_information.downlink', downlink)
        apply_into_json(json_payload, '$[*].event_data.network_information.effective_type', effective_type)
        apply_into_json(json_payload, '$[*].event_data.network_information.rtt', rtt)
        apply_into_json(json_payload, '$[*].event_data.network_load_latency_ms', int(random.randint(288, 578)))
        apply_into_json(json_payload, '$[*].event_data.network_request_latency_ms', int(random.randint(288, 578)))
        apply_into_json(json_payload, '$[*].event_data.network_response_byte_size', int(random.randint(758, 6921)))
        apply_into_json(json_payload, '$[*].event_data.niobe_client_overhead_ms', int(random.randint(0, 4)))
        apply_into_json(json_payload, '$[*].event_data.operation', operation)
        apply_into_json(json_payload, '$[*].event_data.operation_id', operation_id)
        apply_into_json(json_payload, '$[*].event_data.operation_name', operation_name)
        apply_into_json(json_payload, '$[*].event_data.page', page)
        apply_into_json(json_payload, '$[*].event_data.page_name', page_name1)
        apply_into_json(json_payload, '$[*].event_data.page_navigation_action.action_type', action_type)
        apply_into_json(json_payload, '$[*].event_data.page_navigation_action.duration_checkpoint_data.page_view_duration', page_view_duration)
        apply_into_json(json_payload, '$[*].event_data.page_navigation_action.duration_checkpoint_data.total_view_duration', total_view_duration)
        apply_into_json(json_payload, '$[*].event_data.picture_count', picture_count)
        apply_into_json(json_payload, '$[*].event_data.recorder_duration', recorder_duration)
        apply_into_json(json_payload, '$[*].event_data.referrer', referrer)
        apply_into_json(json_payload, '$[*].event_data.remarketing_id', remarketing_id)
        apply_into_json(json_payload, '$[*].event_data.request_strategy', request_strategy)
        apply_into_json(json_payload, '$[*].event_data.schema', schema)
        apply_into_json(json_payload, '$[*].event_data.subject_id', subject_id)
        apply_into_json(json_payload, '$[*].event_data.subject_type', subject_type)
        apply_into_json(json_payload, '$[*].event_data.tbt', tbt)
        apply_into_json(json_payload, '$[*].event_data.total_latency_ms', int(random.randint(0, 582)))
        apply_into_json(json_payload, '$[*].event_data.total_response_latency_ms', int(random.randint(0, 582)))
        apply_into_json(json_payload, '$[*].event_data.treatment', treatment)
        apply_into_json(json_payload, '$[*].event_data.ttfcp', ttfcp)
        apply_into_json(json_payload, '$[*].event_data.ttfmp', ttfmp)
        apply_into_json(json_payload, '$[*].event_data.url', url)
        apply_into_json(json_payload, '$[*].event_data.user_bucket', user_bucket)
        apply_into_json(json_payload, '$[*].event_data.utc_offset', utc_offset)
        apply_into_json(json_payload, '$[*].event_data.uuid', str(uuid.uuid4()))
        apply_into_json(json_payload, '$[*].event_data.value_rating', value_rating)
        apply_into_json(json_payload, '$[*].event_data.visitor_id', visitor_id1)
        apply_into_json(json_payload, '$[*].event_data.web_performance_timing.*', int(random.randint(0, 1636402242423)))
        apply_into_json(json_payload, '$[*].event_data.web_performance_timing.navigation_start_timestamp_in_ms', int(int(time.time() * 1000)))
        apply_into_json(json_payload, '$[*].event_name', event_name1)
        apply_into_json(json_payload, '$[*].schema', schema1)
        apply_into_json(json_payload, '$[*].trackingjs_logging_version', trackingjs_logging_version)
        apply_into_json(json_payload, '$[*].uuid', str(uuid.uuid4()))
        resp = www_airbnb_com_br.post('/tracking/jitney/logging/messages', json=json_payload, headers={'device-memory': device_memory, 'dpr': '2', 'ect': ect, 'viewport-width': viewport_width})
        resp.assert_ok()
        # resp.assert_status_code(204)
        # self.assertLess(resp.elapsed.total_seconds(), 0.221)
