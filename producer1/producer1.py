from kafka import KafkaProducer
import json
from publisher1 import publish
import time 
import socket

def json_serializer(data):
    return json.dumps(data).encode("utf-8") 

SERVER = socket.gethostbyname('kafka1')
SERVER = str(SERVER)+":9092"
producer = KafkaProducer(bootstrap_servers=[SERVER],value_serializer=json_serializer)

if __name__=="__main__":
    while 1 == 1:
       publish_data = publish()
       print(publish_data)
       producer.send("tesla-stock-price",publish_data)
       producer.flush()
       time.sleep(4)

