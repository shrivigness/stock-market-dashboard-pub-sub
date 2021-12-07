from kafka import KafkaConsumer, consumer
import json

if __name__ == "__main__":
    consumer = KafkaConsumer("amazon-stock-price",bootstrap_servers=['localhost:9093'],auto_offset_reset='earliest',group_id="consumer-group-a")
    print("Starting the consumer")
    for msg in consumer:
        #print("Stock price= {}".format(json.loads(msg.value)))
        print("Stock price details of {} is {}".format(msg.topic,json.loads(msg.value)))
        print(msg)