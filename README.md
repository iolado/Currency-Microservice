# CS361 Currency-Microservice

A Python microservice that is able to convert a monetary amount from once currency to another. It uses the API at https://open.er-api.com/v6/latest/. The program accepts from_currency, to_currency, and original_amount. It returns converted_amount, exchange_rate, and rate_date. Data is returned in JSON format.

___________________________________________________________

Requirements
Python 3.10 or newer
Requests
pyzmq

Setup
1) pip install pyzmq requests
or
2) pip install -r requirements.txt

___________________________________________________________

The microservice uses a ZeroMQ REQ/REP communication pattern on port 5473

REQUEST FORMAT

JSON object:
{
    "from_currency": "USD",
    "to_currency": "CAD",
    "origial_amount": 394.22
}

Example

import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5473")

request = {
    "from_currency": "USD",
    "to_currency": "EUR",
    "original_amount": 250
}

socket.send_string(json.dumps(request))

___________________________________________________________

The microservice responds with a JSON object containing the converted data

RESPONSE FORMAT

JSON object:
{
    "from_currency": "USD",
    "to_currency": "EUR",
    "original_amount": 250,
    "converted_amount": 226.66,
    "exchange_rate": 0.91,
    "rate_date": "2026-11-16"
}

Example:

import zmq
import json
from datetime import date

response = {
    "from_currency": from_currency,
    "to_currency": to_currency,
    "original_amount": f"{amount:.2f}",
    "converted_amount": f"{converted_amount:.2f}",
    "exchange_rate": round(rate, 2),
    "rate_date": str(date.today()) 
}

socket.send_string(json.dumps(response))

And the client would receive:

import json

response = socket.recv_string()
print(f"Converted amount: {response}")

___________________________________________________________

