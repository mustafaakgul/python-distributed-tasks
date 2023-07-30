import threading

import time
import random
import atexit
import queue

_queue = queue.Queue(10)

class ProducerThread(threading.Thread):

	def run(self):

		numbers = range(5)
		global _queue

		while True:
			number = random.choice(numbers)
			_queue.put(number)
			print("Produced {}".format(number))
			time.sleep(random.random())


class ConsumerThread(threading.Thread):

	def run(self):
		global _queue
		while True:
			number = _queue.get(0)
			queue.task_done()
			print("Consumed {}".format(number))
			time.sleep(random.random())


producer = ProducerThread()
producer.daemon = True
producer.start()

consumer = ConsumerThread()
consumer.daemon = True
consumer.start()


def exit_handler():
	# refer to https://docs.python.org/3/library/atexit.html
	print("Terminating producer, consumer, mainApp...")


atexit.register(exit_handler)

while True:
	time.sleep(1)
