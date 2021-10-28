import zmq
import json
from pymongo import MongoClient
import pika
import sys 
import os

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def publish(message):
    channel.queue_declare(queue='subscriber1')
    channel.basic_publish(exchange='',routing_key='subscriber1',body=message)
    return 

def callback(ch, method, properties, body):
        message = body.decode('utf8')
        message = json.loads(message)
        print(" [x] Received %r" % message)
        publish(body)
        return

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='publisher')
    
    channel.basic_consume(queue='publisher', on_message_callback=callback, auto_ack=True)

    print('Looking out for messages!')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
