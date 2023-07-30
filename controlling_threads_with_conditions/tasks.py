import threading

import time
import random

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
                print("Queue full, producer is waiting")
                condition.wait()
                print("Space in queue, Consumer notified the producer")
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
                print("Producer added something to queue and notified the consumer")
            number = queue.pop(0)
            print("Consumed {}".format(number))
            condition.notify()
            condition.release()
            time.sleep(random.random())


if __name__ == '__main__':
    producer = ProducerThread()
    consumer = ConsumerThread()
    producer.start()
    consumer.start()
    # producer.join()
    # consumer.join()