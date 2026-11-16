# CS361 Currency-Microservice

#### A Python microservice that is able to convert a monetary amount from one currency to another. It uses the API at https://open.er-api.com/v6/latest/. The program accepts from_currency, to_currency, and original_amount. It returns converted_amount, exchange_rate, and rate_date (the date the exchange rate is retrieved). Data is returned in JSON format.
__________________________________________________________________________________________________

**Requirements**
- Python 3.10 or newer
- Requests
- pyzmq
  


**Setup** \
`pip install pyzmq requests`\
or \
`pip install -r requirements.txt`


**Use a virtual environment to run this service**

Create venv \
`python3 -m venv .venv`

Windows: \
```
.venv\Scripts\activate
<Setup requirement 1 or 2 from above>
```

Mac/Linux: \
```
source .venv/bin/activate <br>
<Setup requirement 1 or 2 from above>
```

__________________________________________________________________________________________________

Communication Method: ZeroMQ REQ/REP\
Port: 5473\
Request data type: JSON\
Response data type: JSON


**REQUEST FORMAT**

JSON object:
```
{
    "from_currency": "USD",
    "to_currency": "CAD",
    "original_amount": 394.22
}
```

Example

```
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
```


The microservice responds with a JSON object containing the converted data

**RESPONSE FORMAT**

JSON object:
```
{
    "from_currency": "USD",
    "to_currency": "EUR",
    "original_amount": 250,
    "converted_amount": 226.66,
    "exchange_rate": 0.91,
    "rate_date": "2026-11-16"
}
```

Example:

```
import zmq
import json
from datetime import date

response = {
    "from_currency": from_currency,
    "to_currency": to_currency,
    "original_amount": round(amount, 2)",
    "converted_amount": round(converted_amount, 2)",
    "exchange_rate": round(rate, 2),
    "rate_date": str(date.today()) 
}

socket.send_string(json.dumps(response))

And the client would receive:

import json

response = socket.recv_string()
data = json.loads(response)

print(f”Converted amount:”, data[converted_amount])
print(f”Exchange Rate:”, data[exchange_rate])
print(f”Rate Date:”, data[rate_date])
```



