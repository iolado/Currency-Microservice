import zmq
import requests


## 0MQ Context
context = zmq.Context()

## Create reply socket
socket = context.socket(zmq.REP)

## bind socket to port 5555
socket.bind("tcp://*:5555")

## send message to client
print("Currency Microservice is running on port 5555...")


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
    response = f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}"
    # Send reply back to client
    socket.send_string(response)
