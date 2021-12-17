import requests
import json


"""Publisher for TESLA's Stock Price"""
def publish():
    url = "https://realstonks.p.rapidapi.com/TSLA"

    headers = {
    'x-rapidapi-host': "realstonks.p.rapidapi.com",
    'x-rapidapi-key': "6c88faa169mshf884cd03d448ab2p151f28jsne5865b21021b"
    }

    response = requests.request("GET", url, headers=headers)
    message = json.loads(response.text)
    return(message)
    
if __name__ == "__main__":
    print(publish())
