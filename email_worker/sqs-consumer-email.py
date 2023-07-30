import smtplib
import time
import json
import boto3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import QUEUE_URL, ACCESS_KEY, SECRET_KEY

sqs = boto3.client('sqs', region_name='ap-southeast-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


gmail_user = "youremail@gmail.com"
gmail_pwd = "yourpassword"


def send_mail(to, subject, text, html, **kwargs):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = gmail_user
    msg['To'] = to
    if kwargs.get('cc', None):
        msg['Cc'] = ','.join(kwargs.get('cc'))
    if kwargs.get('bcc', None):
        msg['Bcc'] = ','.join(kwargs.get('bcc'))
    msg['Subject'] = subject

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    # Put the SMTP connection in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
    mailServer.starttls()

    mailServer.ehlo()
    # Log in on an SMTP server that requires authentication. The arguments are the username and the password
    # if  you get Authentication error from google turn allow less secure applications by navigating to this link : https://myaccount.google.com/lesssecureapps?pli=1
    mailServer.login(gmail_user, gmail_pwd)

    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()


# main entry point to our email worker, imagine running n number of workers concurrently
if __name__ == '__main__':
    print('STARTING WORKER listening on {}'.format(QUEUE_URL))
    while 1:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            AttributeNames=['All'],
            MessageAttributeNames=[
                'string',
            ],
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )
        messages = response.get('Messages', [])
        for message in messages:
            try:
                print('Message Body > ', message.get('Body'))
                body = json.loads(message.get('Body'))
                if not body.get('jobId', None):
                    print('Job Id not provided!')
                    sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message.get('ReceiptHandle'))
                    print('Received and deleted message: {}'.format(message))
                else:
                    job_id = body.get('jobId')
                    print('Running Job Id {}'.format(job_id))
                    # call send mail function to send email
                    send_mail(body.get('to_email'), body.get('subject'), body.get('data').get('text'), body.get('data').get('html'), **{'cc': body.get('cc_email'), 'bcc': body.get('bcc_email')})
                    sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message.get('ReceiptHandle'))
                    print('Received and deleted message: {}'.format(message))
            except Exception as e:
                print('Exception in worker > ', e)

    time.sleep(10)

print('WORKER STOPPED')
