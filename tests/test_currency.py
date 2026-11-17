
import json
from decimal import Decimal

import currency_service as service


def test_valid_conversion(monkeypatch):
    monkeypatch.setattr(
        service,
        "get_exchange_rate",
        lambda source, target: (
            Decimal("0.9"),
            "2026-11-16",
        ),
    )

    result = service.convert_currency({
        "from_currency": "USD",
        "to_currency": "EUR",
        "original_amount": 250,
    })

    assert result["converted_amount"] == 90.00
    assert result["exchange_rate"] == 0.9
    assert result["rate_date"] == "2026-11-16"


def test_currency_codes_uppercase(monkeypatch):
    monkeypatch.setattr(
        service,
        "get_exchange_rate",
        lambda source, target: (
            Decimal("1"),
            "2026-11-16",
        ),
    )

    result = service.convert_currency({
        "from_currency": "usd",
        "to_currency": "USD",
        "original_amount": 50,
    })

    assert result["from_currency"] == "USD"
    assert result["to_currency"] == "USD"


def test_missing_amount():
    result = service.process_request(json.dumps({
        "from_currency": "USD",
        "to_currency": "EUR",
    }))

    assert "error" in result


def test_invalid_currency():
    result = service.process_request(json.dumps({
        "from_currency": "INVALID",
        "to_currency": "EUR",
        "original_amount": 100,
    }))

    assert "error" in result


def test_negative_amount():
    result = service.process_request(json.dumps({
        "from_currency": "USD",
        "to_currency": "EUR",
        "original_amount": -100,
    }))

    assert "error" in result


def test_invalid_json():
    result = service.process_request("not valid JSON")

    assert "error" in result


def test_invalid_numeric_amount():
    result = service.process_request(json.dumps({
        "from_currency": "USD",
        "to_currency": "EUR",
        "original_amount": "abc",
    }))

    assert "error" in result


def test_api_failure(monkeypatch):
    import requests

    def failing_rate(source, target):
        raise requests.exceptions.Timeout()

    monkeypatch.setattr(
        service,
        "get_exchange_rate",
        failing_rate,
    )

    result = service.process_request(json.dumps({
        "from_currency": "USD",
        "to_currency": "EUR",
        "original_amount": 100,
    }))

    assert "error" in result
