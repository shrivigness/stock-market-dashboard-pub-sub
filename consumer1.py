from kafka import KafkaConsumer, consumer
import json

if __name__ == "__main__":
    consumer = KafkaConsumer("tesla-stock-price",bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',group_id="consumer-group-a")
    print("Starting the consumer")
    listoftopics = KafkaConsumer(bootstrap_servers=['localhost:9092'])
    print(listoftopics.topics())
    for msg in consumer:
        #print("Stock price= {}".format(json.loads(msg.value)))
        print("Stock price details of {} is {} with offset of {} in partition {}".format(msg.topic,json.loads(msg.value),msg.offset,msg.partition))
        