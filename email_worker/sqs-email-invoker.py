import json
import boto3
import uuid

from .config import QUEUE_URL, ACCESS_KEY, SECRET_KEY

sqs = boto3.client('sqs', region_name='ap-southeast-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)


def send_sample_email():

	# Create the body of the message (a plain-text and an HTML version).
	text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.tiptapcode.com"
	html = """\
	<html>
		<head></head>
			<body>
				<p>Hi!<br>
					How are you?<br>
					Here is the <a href="http://www.tiptapcode.com">link</a> you wanted.
				</p>
			</body>
	</html>
	"""

	# for simplicity we could try converting this into a single dictionary object give that a try
	to_email = "sevan43@villabhj.com"
	subject = "<subject>"
	cc_email = ['d9qvor+20xckoq17bmr0@sharklasers.com', 'd9qwp9+35h5rokgpwls@guerrillamail.info']
	bcc_email = ['d9pu46+l8ksnk5o@sharklasers.com']

	body = json.dumps({'jobId': str(uuid.uuid4()), 'to_email': to_email, 'subject': subject, 'cc_email': cc_email, 'bcc_email': bcc_email, 'data': {'text': text, 'html': html}})
	res = sqs.send_message(
		QueueUrl=QUEUE_URL,
		MessageBody=body
	)
	print(res)
	print('SUCCESS')


send_sample_email()
