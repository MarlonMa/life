#!/usr/bin/env python
"""The toolbox defines objects which can be used universally.
"""


def get_url(url):
    import requests
    res = requests.get(url)
    res.encoding = 'utf-8'
    return res


def send_mail(subject, content, smtp_server='smtp.yeah.net', port=25, sender='marlonm@yeah.net', password=None, receiver=['marlonm@yeah.net'], cc_receiver=[]):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from smtplib import SMTP as smtp
    from smtplib import SMTPServerDisconnected
    all_receivers = receiver + cc_receiver
    container = MIMEMultipart('alternative')
    container['Subject'] = subject
    container['From'] = sender
    container['To'] = ', '.join(receiver)
    container['CC'] = ', '.join(cc_receiver)
    content_plain = MIMEText(content, 'html')
    container.attach(content_plain)
    smtp_conn = smtp(smtp_server, port)
    smtp_conn.ehlo()
    smtp_conn.starttls()
    smtp_conn.login(sender, password)
    smtp_conn.sendmail(sender, all_receivers, container.as_string())
    smtp_conn.quit()
