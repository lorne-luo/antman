import os
from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load operating system environment variables and then prepare to use them
env = Env()
env.read_env('.env')

ADMIN_MOBILE_NUMBER = env('ADMIN_MOBILE_NUMBER', default='')
ADMIN_EMAIL = env('ADMIN_EMAIL', default='')

# TELSTRA SMS API KEY
# ------------------------------------------------------------------------------
TELSTRA_CLIENT_KEY = env('TELSTRA_CLIENT_KEY', default='')
TELSTRA_CLIENT_SECRET = env('TELSTRA_CLIENT_SECRET', default='')

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

# ALIYUN EMAIL
# ------------------------------------------------------------------------------
ALIYUN_EMAIL_HOST = env('ALIYUN_EMAIL_HOST', default='smtpdm-ap-southeast-2.aliyun.com')
ALIYUN_SINGLE_EMAIL_USERNAME = env('ALIYUN_SINGLE_EMAIL_USERNAME', default='')  # 发件人地址，通过控制台创建的发件人地址
ALIYUN_SINGLE_EMAIL_PASSWORD = env('ALIYUN_SINGLE_EMAIL_PASSWORD', default='')  # 发件人密码，通过控制台创建的发件人密码
# 批量发信地址
ALIYUN_BATCH_EMAIL_USERNAME = env('ALIYUN_BATCH_EMAIL_USERNAME', default='')
ALIYUN_BATCH_EMAIL_PASSWORD = env('ALIYUN_BATCH_EMAIL_PASSWORD', default='')
