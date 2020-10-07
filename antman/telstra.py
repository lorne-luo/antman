import json
import logging
import time
import Telstra_Messaging
from datetime import datetime, timedelta
from Telstra_Messaging.rest import ApiException
from . import configs

log = logging.getLogger(__name__)

TELSTRA_LENGTH_PER_SMS = 160
TELSTRA_MONTHLY_FREE_LIMIT = 1000
TELSTRA_ACCESS_TOKEN = None
TELSTRA_ACCESS_TOKEN_EXPIRY = datetime.utcnow()
TELSTRA_DESTINATION_ADDRESS = None
TELSTRA_DESTINATION_ADDRESS_EXPIRY = datetime.utcnow()


def get_token():
    global TELSTRA_ACCESS_TOKEN, TELSTRA_ACCESS_TOKEN_EXPIRY
    access_token = TELSTRA_ACCESS_TOKEN if TELSTRA_ACCESS_TOKEN_EXPIRY > datetime.now() else None
    if access_token:
        return access_token

    configuration = Telstra_Messaging.Configuration()
    api_instance = Telstra_Messaging.AuthenticationApi(Telstra_Messaging.ApiClient(configuration))
    client_id = configs.TELSTRA_CLIENT_KEY
    client_secret = configs.TELSTRA_CLIENT_SECRET
    grant_type = 'client_credentials'

    try:
        # Generate OAuth2 token
        api_response = api_instance.auth_token(client_id, client_secret, grant_type)
        access_token = api_response.access_token
        expires_in = int(api_response.expires_in) if api_response.expires_in.isdigit() else 3599
        TELSTRA_ACCESS_TOKEN = access_token
        TELSTRA_ACCESS_TOKEN_EXPIRY = datetime.now() + timedelta(seconds=expires_in)
        return access_token
    except ApiException as e:
        log.error("Exception when calling AuthenticationApi->auth_token: %s\n" % e)
        return None


def get_from_number():
    global TELSTRA_DESTINATION_ADDRESS, TELSTRA_DESTINATION_ADDRESS_EXPIRY
    destination_address = TELSTRA_DESTINATION_ADDRESS if TELSTRA_DESTINATION_ADDRESS_EXPIRY > datetime.now() else None
    if destination_address:
        return destination_address

    configuration = Telstra_Messaging.Configuration()
    configuration.access_token = get_token()
    api_instance = Telstra_Messaging.ProvisioningApi(Telstra_Messaging.ApiClient(configuration))
    provision_number_request = Telstra_Messaging.ProvisionNumberRequest()  # ProvisionNumberRequest | A JSON payload containing the required attributes
    api_response = api_instance.create_subscription(provision_number_request)
    destination_address = api_response.destination_address
    expiry_timestamp = int(api_response.expiry_date / 1000)
    expires_in = expiry_timestamp - int(time.mktime(datetime.now().timetuple()))
    TELSTRA_DESTINATION_ADDRESS = destination_address
    TELSTRA_DESTINATION_ADDRESS_EXPIRY = datetime.now() + timedelta(seconds=expires_in)
    return destination_address


def register_free_trial_bnum():
    configuration = Telstra_Messaging.Configuration()
    configuration.access_token = get_token()
    api_client = Telstra_Messaging.ApiClient(configuration)

    url = 'https://tapi.telstra.com/v2/messages/freetrial/bnum'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'User-Agent': 'OpenAPI-Generator/1.0.7/python',
               'Authorization': 'Bearer JzW3OGXwQMhlXXsRNosuVbG7QHLR'}
    body = {"bnum": [
        "+61413725868",
    ]}
    response = api_client.rest_client.POST(url,
                                           query_params=[],
                                           headers=headers,
                                           post_params=[],
                                           _preload_content=True,
                                           _request_timeout=None,
                                           body=body)

    data = json.loads(response.data)
    status = response.status
    headers = response.getheaders()
    return data


def get_free_trial_bnum():
    configuration = Telstra_Messaging.Configuration()
    configuration.access_token = get_token()
    api_client = Telstra_Messaging.ApiClient(configuration)

    url = 'https://tapi.telstra.com/v2/messages/freetrial/bnum'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'User-Agent': 'OpenAPI-Generator/1.0.7/python',
               'Authorization': 'Bearer JzW3OGXwQMhlXXsRNosuVbG7QHLR'}

    response = api_client.rest_client.GET(url,
                                          query_params=[],
                                          headers=headers,
                                          _preload_content=True,
                                          _request_timeout=None)
    data = json.loads(response.data)
    status = response.status
    headers = response.getheaders()
    return data


def validate_au_mobile(mobile):
    if not mobile:
        return ''
    mobile = mobile.strip()
    if mobile.startswith('+61'):
        mobile = mobile.replace('+61', '')
    if mobile.startswith('061'):
        mobile = mobile.replace('061', '')
    if mobile.startswith('0061'):
        mobile = mobile.replace('0061', '')
    if mobile.startswith('4'):
        mobile = '0' + mobile
    if mobile.startswith('04') and len(mobile) == len('0413725868'):
        return mobile
    return ''


def send_au_sms(to, body, app_name=None):
    counter = 0
    if not counter < TELSTRA_MONTHLY_FREE_LIMIT:
        log.info('[SMS] Telstra SMS reach 1000 free limitation.')
        return False, 'Telstra SMS reach 1000 free limitation.'

    to = validate_au_mobile(to)
    if not to:
        return False, 'INVALID_PHONE_NUMBER'

    body = str(body)
    if not body:
        return False, 'EMPTY_CONTENT'

    # Configure OAuth2 access token for authorization: auth
    configuration = Telstra_Messaging.Configuration()
    configuration.access_token = get_token()
    from_number = get_from_number()

    # api_instance = Telstra_Messaging.ProvisioningApi(Telstra_Messaging.ApiClient(configuration))
    # provision_number_request = Telstra_Messaging.ProvisionNumberRequest()  # ProvisionNumberRequest | A JSON payload containing the required attributes
    api_instance = Telstra_Messaging.MessagingApi(Telstra_Messaging.ApiClient(configuration))
    send_sms_request = Telstra_Messaging.SendSMSRequest(to, body, from_number)

    try:
        # {'country': [{u'AUS': 1}],
        #  'message_type': 'SMS',
        #  'messages': [{'delivery_status': 'MessageWaiting',
        #                'message_id': 'd872ad3b000801660000000000462650037a0801-1261413725868',
        #                'message_status_url': 'https://tapi.telstra.com/v2/messages/sms/d872ad3b000801660000000000462650037a0801-1261413725868/status',
        #                'to': '+61413725868'}],
        #  'number_segments': 1}
        api_response = api_instance.send_sms(send_sms_request)
        success = api_response.messages[0].delivery_status == 'MessageWaiting'

        if success:
            return True, 'MessageWaiting'
    except ApiException as e:
        log.error("Exception when calling MessagingApi->send_sms: %s\n" % e)
        return False, str(e)


def send_to_admin(body, app_name=None):
    send_au_sms(configs.ADMIN_MOBILE_NUMBER, body, app_name)
