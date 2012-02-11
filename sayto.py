# !/usr/bin python
# coding=utf-8

import smtplib
import sys
import os
import datetime
import config

def main():
    if len(sys.argv) != 3:
        return
    s =smtplib.SMTP(config.SMTP_SERVER_ADDR,
            config.SMTP_SERVER_PORT, timeout=10)
    s.ehlo()
    s.starttls()
    s.login(config.SMTP_USER_NAME, config.SMTP_USER_PWD)

    to_addr = sys.argv[1]
    if to_addr.find('@') == -1:
        if config.DEFAULT_RECIPIENTS.has_key(to_addr):
            to_addr = config.DEFAULT_RECIPIENTS[to_addr]
        else:
            return

    file_path = sys.argv[2]
    if not os.path.exists(file_path):
        return

    with open(file_path) as f:
        subject = f.readline()
        if subject is '':
            return

        body = ''.join(f.readlines())

        header = 'To:' + to_addr + '\n' + \
                'From:' + config.AUTHOR_ADDR + '\n' + \
                'Subject:' + subject + '\n'

        message = header + '\n' + body

        s.sendmail(config.AUTHOR_ADDR, to_addr, message)
        print '[x] %r Mail has been sent.' % (datetime.datetime.now().ctime(),)
        

if __name__ == '__main__':
    main()
