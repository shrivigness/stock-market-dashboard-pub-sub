import time
import requests
import json
import pika

"""Publisher for Apple's stock summary"""


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"
querystring = {"symbol":"AAPL","region":"US"}

headers = {
    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }

response = ''

response = requests.request("GET", url, headers=headers, params=querystring)
message = response.json()
message["Topic"] = 'Apple stock summary'
message["Sender"] = 'Publisher3'
message = json.dumps(message)    
time.sleep(2)
print(type(message))
channel.queue_declare(queue='publisher')
channel.basic_publish(exchange='',routing_key='publisher',body=message)
print(" [x] Sent 'Hello World!'")

