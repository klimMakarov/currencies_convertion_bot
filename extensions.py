import requests
import json
from config import currencies


class APIException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base_ticker, quote_ticker = base.upper(), quote.upper()
        if base_ticker not in currencies.keys():
            raise APIException(f"Валюты <{base}> нет в списке доступных")
        if quote_ticker not in currencies.keys():
            raise APIException(f"Валюты <{quote}> нет в списке доступных")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Некорректное кол-во: <{amount}>")

        request = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_quote = json.loads(request.content)[quote_ticker]
        return float(total_quote)
