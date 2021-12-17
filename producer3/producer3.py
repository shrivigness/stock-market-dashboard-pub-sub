from kafka import KafkaProducer
import json
from publisher3 import publish
import time 

def json_serializer(data):
    return json.dumps(data).encode("utf-8") 

producer = KafkaProducer(bootstrap_servers=['kafka3:19094'],value_serializer=json_serializer)

if __name__=="__main__":
    while 1 == 1:
       publish_data = publish()
       print(publish_data)
       producer.send("apple-stock-price",publish_data)
       time.sleep(4)

