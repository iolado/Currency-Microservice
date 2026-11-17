
import json
import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5473")

    # Prevent waiting forever if the service is unavailable
    socket.setsockopt(zmq.RCVTIMEO, 10000)
    socket.setsockopt(zmq.SNDTIMEO, 10000)
    socket.setsockopt(zmq.LINGER, 0)

    try:
        from_currency = input(
            "Enter source currency (e.g., USD): "
        )

        to_currency = input(
            "Enter target currency (e.g., EUR): "
        )

        amount = input(
            "Enter amount to convert: "
        )

        request_data = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "original_amount": amount,
        }

        print("\nSending request:")
        print(json.dumps(request_data, indent=2))

        socket.send_json(request_data)

        response = socket.recv_json()

        print("\nReceived response:")
        print(json.dumps(response, indent=2))

        if "error" in response:
            print("\nConversion failed:", response["error"])
        else:
            print(
                "\nConverted amount:",
                response["converted_amount"],
                response["to_currency"],
            )

    except zmq.Again:
        print("Error: Microservice did not respond in time.")

    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    main()