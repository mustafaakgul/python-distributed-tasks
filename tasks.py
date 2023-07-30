import time
import redis

from datetime import timedelta
from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab


app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')


@app.task(name='tasks.add')
def add(x, y):
	total = x + y
	print('{} + {} = {}'.format(x, y, total))
	time.sleep(10)
	return total


def backoff(attempts):
	"""
	1, 2, 4, 8, 16, 32...
	"""
	return 2 ** attempts


@app.task(bind=True, max_retries=4, soft_time_limit=5)
def data_extractor(self):
	try:
		for i in range(1, 11):
			print('Crawling HMTL DOM!')
			if i == 5:
				raise ValueError('Crawling Index Error')
	except Exception as exc:
		print('There was an exception lets retry after 5 seconds')
		raise self.retry(exc=exc, countdown=backoff(self.request.retries))


@periodic_task(bind=True, run_every=timedelta(seconds=10), name="tasks.send_mail_from_queue_simple")
def send_mail_from_queue_simple(self):
	try:
		messages_sent = "example.email"
		print("{} Email message successfully sent, [{}]".format(self.request.hostname, messages_sent))
	finally:
		print("release resources")


@periodic_task(run_every=(crontab(day_of_week='sunday', minute='*/1')), name="tasks.send_mail_in_queue_task", ignore_result=True)
def send_mail_queue():
	try:
		messages_sent = "example.email"
		print("Total email message successfully sent %d.", messages_sent)
	finally:
		print("release resources")


key = "4088587A2CAB44FD902D6D5C98CD2B17"


@periodic_task(bind=True, run_every=timedelta(seconds=5), name="tasks.send_mail_from_queue")
def send_mail_from_queue(self):
	REDIS_CLIENT = redis.Redis()
	timeout = 60 * 5  # Lock expires in 5 minutes
	have_lock = False
	my_lock = REDIS_CLIENT.lock(key, timeout=timeout)
	try:
		have_lock = my_lock.acquire(blocking=False)
		if have_lock:
			messages_sent = "example.email"
			print("{} Email message successfully sent, [{}]".format(self.request.hostname, messages_sent))
			time.sleep(10)
	finally:
		print("release resources")
		if have_lock:
			my_lock.release()
