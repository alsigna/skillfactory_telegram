from config import CURRENCIES
from extensions import ExchangeException
import requests


def get_available_currencies() -> str:
    available_currency = "Доступные валюты:\n"

    table_header = ["Название", "Тикер"]
    max_name_len = max(map(len, list(CURRENCIES.keys())))
    max_name_len = max(max_name_len, len(table_header[0])) + 2
    currency_table = "```\n"
    currency_table += f"{'|':-<{max_name_len}}-+-------|\n"
    currency_table += f"|{table_header[0]: ^{max_name_len}}| {table_header[1]} |\n"
    currency_table += f"{'|':-<{max_name_len}}-+-------|\n"
    for name, ticker in CURRENCIES.items():
        currency_table += f"| {name: <{max_name_len-1}}|  {ticker}  |\n"
    currency_table += f"{'|':-<{max_name_len}}-+-------|\n"
    currency_table += "```"

    return available_currency + currency_table


def get_help() -> str:
    hello_msg = (
        "Что бы начать работу введите команду в следующем формате\n"
        "`<исходная валюта> <в какую валюту переводим> <количество исходной валюты>`\n"
        "валюта указывается названием (Рубль, Доллар ...) или тикером (RUB, USD ...) в любом регистре\n"
        "/help - помощь\n"
        "/currencies - список доступных валют\n"
    )
    return hello_msg


def validate_input_data(command: str) -> list:
    words = command.split()
    if len(words) != 3:
        raise ExchangeException("неверный формат входных данных. /help - помощь")
    words = list(map(str.lower, words))
    fsym, tsyms, amount = words

    if fsym not in CURRENCIES.keys() and fsym not in CURRENCIES.values():
        raise ExchangeException("неизвестная исходная валюта. /currencies - список доступных валют")
    fsym = CURRENCIES.get(fsym, fsym)

    if tsyms not in CURRENCIES.keys() and tsyms not in CURRENCIES.values():
        raise ExchangeException("неизвестная валюта перевода. /currencies - список доступных валют")
    tsyms = CURRENCIES.get(tsyms, tsyms)

    try:
        float(amount)
    except ValueError:
        raise ExchangeException("количество исходное валюты должно быть числом, челым или дробным (с точкой)")

    return [fsym, tsyms, amount]


def exchange_inputs(fsym: str, tsyms: str, amount: str) -> str:
    url = f"https://min-api.cryptocompare.com/data/price?fsym={fsym}&tsyms={tsyms}"
    response = requests.get(url)
    rate = response.json().get(tsyms.upper(), None)
    if rate is None:
        return "😢 сервис конвертации недоступен"
    famount = round(float(amount), 2)
    tamount = round(famount * rate, 2)
    return f"{famount} {fsym} это {tamount} {tsyms}"
