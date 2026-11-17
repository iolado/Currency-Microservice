
import json
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import requests
import zmq

PORT = 5473
API_URL = "https://open.er-api.com/v6/latest/"
TIMEOUT = 5


def error_response(message):
    return {"error": message}


def validate_request(data):
    """Validate incoming JSON conversion data."""
    if not isinstance(data, dict):
        raise ValueError("Request must be a JSON object")

    required = [
        "from_currency",
        "to_currency",
        "original_amount",
    ]

    for field in required:
        if field not in data:
            raise ValueError(f"Missing field: {field}")

    source = data["from_currency"]
    target = data["to_currency"]

    if not isinstance(source, str) or not re.fullmatch(
        r"[A-Za-z]{3}", source.strip()
    ):
        raise ValueError("Invalid source currency code")

    if not isinstance(target, str) or not re.fullmatch(
        r"[A-Za-z]{3}", target.strip()
    ):
        raise ValueError("Invalid target currency code")

    if isinstance(data["original_amount"], bool):
        raise ValueError("Invalid amount")

    try:
        amount = Decimal(str(data["original_amount"]))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Amount must be numeric") from None

    if not amount.is_finite() or amount < 0:
        raise ValueError("Amount must be finite and nonnegative")

    return source.strip().upper(), target.strip().upper(), amount

def get_exchange_rate(source, target):
    """Retrieve an exchange rate from the external API."""
    response = requests.get(
        f"{API_URL}{source}",
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError("Exchange-rate provider rejected the request")

    rates = data.get("rates", {})

    if target not in rates:
        raise ValueError("Unsupported target currency")

    rate = Decimal(str(rates[target]))

    if not rate.is_finite() or rate <= 0:
        raise ValueError("Invalid exchange rate received")

    timestamp = data.get("time_last_update_utc")

    if timestamp:
        try:
            rate_date = datetime.strptime(
                timestamp, "%a, %d %b %Y %H:%M:%S %z"
            ).date().isoformat()
        except ValueError:
            rate_date = None
    else:
        rate_date = None

    return rate, rate_date


def convert_currency(data):
    """Validate a request and calculate the conversion."""
    source, target, amount = validate_request(data)

    rate, rate_date = get_exchange_rate(source, target)

    converted = (amount * rate).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    rounded_amount = amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "from_currency": source,
        "to_currency": target,
        "original_amount": float(rounded_amount),
        "converted_amount": float(converted),
        "exchange_rate": float(rate),
        "rate_date": rate_date,
    }


def process_request(message):
    """Process one JSON request and always return JSON data."""
    try:
        data = json.loads(message)
        return convert_currency(data)

    except json.JSONDecodeError:
        return error_response("Invalid JSON request")

    except ValueError as exc:
        return error_response(str(exc))

    except requests.exceptions.RequestException:
        return error_response(
            "Exchange-rate provider is unavailable"
        )

    except (KeyError, TypeError, InvalidOperation):
        return error_response("Invalid exchange-rate data")


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")

    print(f"Currency Microservice running on port {PORT}")

    try:
        while True:
            message = socket.recv_string()
            print("Received request:", message)

            result = process_request(message)

            socket.send_string(json.dumps(result))

    except KeyboardInterrupt:
        print("\nStopping Currency Microservice")

    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()
