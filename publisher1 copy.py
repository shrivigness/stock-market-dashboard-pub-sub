import time
import requests
import json
import pymongo

"""Publisher for TESLA's Stock Price"""
client = pymongo.MongoClient("mongodb://localhost:27017")
url = "https://realstonks.p.rapidapi.com/TSLA"

headers = {
    'x-rapidapi-host': "realstonks.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }
def Publish():
    response = requests.request("GET", url, headers=headers)
    message = json.loads(response.text)
    #print(message)
    message = json.loads(message)
    #print(type(message))
    message["Topic"] = "Tesla stock price"
    message["Sender"] = "Publisher1"
    print('Publisher1 sending Payload to DB:' + json.dumps(message))
    #db = client.get_database('total_records')
    #records = db.register
    return
    
if __name__ == "__main__":
    time.sleep(3)
    while(1):
        Publish()
        time.sleep(15)
