from kafka import KafkaProducer
import json
from publisher2 import publish
import time 

def json_serializer(data):
    return json.dumps(data).encode("utf-8") 

SERVER = socket.gethostbyname('IP1')
producer = KafkaProducer(bootstrap_servers=['kafka2:19093'],value_serializer=json_serializer)

if __name__=="__main__":
    while 1 == 1:
       publish_data = publish()
       print(publish_data)
       producer.send("amazon-stock-price",publish_data)
       time.sleep(4)

