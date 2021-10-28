import time
import requests
import json
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

url = "https://yh-finance.p.rapidapi.com/stock/v2/get-chart"

querystring = {"interval":"5m","symbol":"AMZN","range":"1d","region":"US"}

headers = {
    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }
response = ''

response = requests.request("GET", url, headers=headers, params=querystring)
message = response.json()
message["Topic"] = 'Amazon stock summary'
message["Sender"] = 'Publisher2'
message = json.dumps(message)
time.sleep(2)
print(type(message))
channel.queue_declare(queue='publisher')
channel.basic_publish(exchange='',routing_key='publisher',body=message)
print(" [x] Sent 'Hello World!'")
