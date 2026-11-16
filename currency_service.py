import zmq
import requests
from datetime import date
import json


## 0MQ Context
context = zmq.Context()

## Create reply socket
socket = context.socket(zmq.REP)

## bind socket to port 5473
socket.bind("tcp://*:5473")

## send message to client
print("Currency Microservice is running on port 5473...")


def get_exchange_rates(from_currency, to_currency):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"

    response = requests.get(url)
    data = response.json()

    return data["rates"][to_currency]

while True:
    # Wait for next request from client
    message = socket.recv_string()
    print(f"Received request: {message}")

    ## expected input:
    ## USD,EUR,100
    from_currency, to_currency, amount = message.split(',')
    amount = float(amount)

    rate = get_exchange_rates(from_currency, to_currency)
    converted_amount = amount * rate

    # Process the conversion and prepare the response
    response = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "original_amount": f"{amount:.2f}",
        "converted_amount": f"{converted_amount:.2f}",
        "exchange_rate": round(rate, 2),
        "rate_date": str(date.today()) 
    }

    # Send reply back to client
    socket.send_string(json.dumps(response))
