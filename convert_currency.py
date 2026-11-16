import zmq

## 0MQ Context
context = zmq.Context()

## Create request socket
socket = context.socket(zmq.REQ)

## connect to the server
socket.connect("tcp://localhost:5555")

## send request to the server
from_currency = input("Enter the source currency code (e.g., USD): ")
to_currency = input("Enter the target currency code (e.g., EUR): ")
amount = input("Enter the amount to convert (e.g., 100): ")
request_message = f"{from_currency},{to_currency},{amount}"
print(f"Sending request: {request_message}")

## send request to the server
socket.send_string(request_message)

## receive response from the server
response = socket.recv_string()
print(f"Converted amount: {response}")