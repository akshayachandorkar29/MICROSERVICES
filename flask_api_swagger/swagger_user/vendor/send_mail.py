"""
This file contains business logic to send the mail using SMTP server
Author: Akshaya Revaskar
Date: 28/04/2020
"""

# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from ..swagger_env import Configuration
configuration = Configuration()


class SendMail:

    def __init__(self):
        pass

    def send_mail(self, to_mail, message):
        try:
            # create message object instance
            msg = MIMEMultipart()

            # setup the parameters of the message
            password = configuration.MICRO_EMAIL_PASSWORD
            msg['From'] = configuration.MICRO_EMAIL_FROM
            msg['To'] = to_mail
            msg['Subject'] = "Link"

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # create server
            server = smtplib.SMTP('smtp.gmail.com: 587')

            server.starttls()

            # Login Credentials for sending the mail
            server.login(msg['From'], password)

            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())

            server.quit()

            print("successfully sent email to %s:" % (msg['To']))

        except Exception as e:
            print(e)
