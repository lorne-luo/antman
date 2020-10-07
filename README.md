ANTMAN
===============================

version number: 0.0.1
author: Lorne

Overview
--------

Notification library

Installation
--------------------

To install use pip:

    $ pip install git+https://github.com/lorne-luo/antman.git


Usage
--------------------

    # send email
    from antman.aliyun.email.smtp import *
    send_email('test@test.com','test email','this is a test email')

    # send au sms
    from antman.telstra import *
    send_to_admin('test msg')
