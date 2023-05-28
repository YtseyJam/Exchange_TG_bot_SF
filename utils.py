import requests
import json
from config import keys, EXCHANGE_API


class ConvertionExeption(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption("‼️Вы пытаетесь перевести одинаковые валюты")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'‼️Не могу обработать валюту – {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'‼️Не могу обработать валюту – {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'‼️Не удалось обработать количество {amount}.\nТребуется числовое значение. Возможно, введена запятая вместо точки?')


        r = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API}/pair/{quote_ticker}/{base_ticker}/{amount}")
        total_base = json.loads(r.content)['conversion_result']

        return total_base

class RoubleCourse:
    @staticmethod
    def get_rouble():
        usd = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API}/latest/USD")
        eur = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API}/latest/EUR")
        cny = requests.get(f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API}/latest/CNY")

        usd_base = json.loads(usd.content)["conversion_rates"]["RUB"]
        eur_base = json.loads(eur.content)["conversion_rates"]["RUB"]
        cny_base = json.loads(cny.content)["conversion_rates"]["RUB"]
        return usd_base, eur_base, cny_base
