import os
from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load operating system environment variables and then prepare to use them
env = Env()
env.read_env('.env')

# TELSTRA SMS API KEY
# ------------------------------------------------------------------------------
TELSTRA_CLIENT_KEY = env('TELSTRA_CLIENT_KEY', default='')
TELSTRA_CLIENT_SECRET = env('TELSTRA_CLIENT_SECRET', default='')
ADMIN_MOBILE_NUMBER = env('ADMIN_MOBILE_NUMBER', default='')

# SENDGRID EMAIL API
# ------------------------------------------------------------------------------
SENDGRID_API_KEY = env('SENDGRID_API_KEY', default='')

# ALIYUN SMS
# ------------------------------------------------------------------------------
ALIYUN_ACCESS_KEY_ID = env('ALIYUN_ACCESS_KEY_ID', default='')
ALIYUN_ACCESS_KEY_SECRET = env('ALIYUN_ACCESS_KEY_SECRET', default='')

ORDER_SENT_PAID_TEMPLATE = 'SMS_150172602'
ORDER_SENT_UNPAID_TEMPLATE = 'SMS_150172601'
ORDER_DELIVERED_TEMPLATE = 'SMS_142060006'
PACKAGE_DELIVERED_TEMPLATE = 'SMS_142050123'
VERIFICATION_CODE_TEMPLATE = 'SMS_116567674'

# TELEGRAM
# ------------------------------------------------------------------------------
TELEGRAM_TOKEN = env('TELEGRAM_TOKEN', default='')
