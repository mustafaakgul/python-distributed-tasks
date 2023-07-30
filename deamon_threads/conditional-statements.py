import threading

import time
import random
import atexit

queue = []
MAX_ITEMS = 10

condition = threading.Condition()


class ProducerThread(threading.Thread):

	def run(self):

		numbers = range(5)
		global queue

		while True:
			condition.acquire()
			if len(queue) == MAX_ITEMS:
				print("Queue is full, producer is waiting")
				condition.wait()
				print("Space in queue, Consumer notified producer")
			number = random.choice(numbers)
			queue.append(number)
			print("Produced {}".format(number))
			condition.notify()
			condition.release()
			time.sleep(random.random())


class ConsumerThread(threading.Thread):

	def run(self):
		global queue
		while True:
			condition.acquire()
			if not queue:
				print("Nothing in queue, consumer is waiting")
				condition.wait()
				print ("Producer added something to queue and notify the consumer")

			number = queue.pop(0)
			print("Consumed {}".format(number))
			condition.notify()
			condition.release()
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
