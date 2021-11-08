from up9lib import *
from authentication import authenticate

# logging.basicConfig(level=logging.DEBUG)


@data_driven_tests
class Tests_notify_bugsnag_com(unittest.TestCase):

    @json_dataset('data/20/dataset_20.json')
    @clear_session({'spanId': 20})
    def test_20_post_(self, data_row):
        apiKey, bev, bugsnag_api_key, bugsnag_payload_version, bugsnag_sent_at, clientIp, connection_type, duration, errorMessage, experiments, id_, id1, id2, message, name, payloadVersion, startedAt, time_, timestamp, treatments, trebuchets, url, url1, userAgent, values, version, version1 = data_row

        # POST https://notify.bugsnag.com/ (endp 20)
        notify_bugsnag_com = get_http_client('https://notify.bugsnag.com', authenticate)
        with open('data/20/payload_for_endp_20.json', 'r') as json_payload_file:
            json_payload = json.load(json_payload_file)
        apply_into_json(json_payload, '$.apiKey', apiKey)
        apply_into_json(json_payload, '$.events[*].app.duration', duration)
        apply_into_json(json_payload, '$.events[*].app.version', version)
        apply_into_json(json_payload, '$.events[*].breadcrumbs[*].name', name)
        apply_into_json(json_payload, '$.events[*].breadcrumbs[*].timestamp', timestamp)
        apply_into_json(json_payload, '$.events[*].device.id', id_)
        apply_into_json(json_payload, '$.events[*].device.time', time_)
        apply_into_json(json_payload, '$.events[*].device.userAgent', userAgent)
        apply_into_json(json_payload, '$.events[*].exceptions[*].errorMessage', errorMessage)
        apply_into_json(json_payload, '$.events[*].exceptions[*].message', message)
        apply_into_json(json_payload, '$.events[*].metaData.*.experiments[*]', experiments)
        apply_into_json(json_payload, '$.events[*].metaData.*.treatments[*]', treatments)
        apply_into_json(json_payload, '$.events[*].metaData.connection_type', connection_type)
        apply_into_json(json_payload, '$.events[*].metaData.trebuchets.trebuchets[*]', trebuchets)
        apply_into_json(json_payload, '$.events[*].metaData.trebuchets.values[*]', values)
        apply_into_json(json_payload, '$.events[*].metaData.user.bev', bev)
        apply_into_json(json_payload, '$.events[*].payloadVersion', payloadVersion)
        apply_into_json(json_payload, '$.events[*].request.clientIp', clientIp)
        apply_into_json(json_payload, '$.events[*].request.url', url)
        apply_into_json(json_payload, '$.events[*].session.id', id1)
        apply_into_json(json_payload, '$.events[*].session.startedAt', startedAt)
        apply_into_json(json_payload, '$.events[*].user.id', id2)
        apply_into_json(json_payload, '$.notifier.url', url1)
        apply_into_json(json_payload, '$.notifier.version', version1)
        resp = notify_bugsnag_com.post('/', json=json_payload, headers={'bugsnag-api-key': bugsnag_api_key, 'bugsnag-payload-version': bugsnag_payload_version, 'bugsnag-sent-at': bugsnag_sent_at})
        resp.assert_ok()
        # resp.assert_status_code(200)
        # self.assertLess(resp.elapsed.total_seconds(), 0.377)
