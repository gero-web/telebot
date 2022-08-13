import requests

data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()


class APIException(Exception):
    pass


class Convert:

    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            return amount
        if base == 'RUB':
            return round(amount / data['Valute'][quote]['Value'], 4)
        elif quote == 'RUB':
            return round(amount * data['Valute'][base]['Value'], 4)

        result = amount * data['Valute'][base]['Value'] / data['Valute'][quote]['Value']
        return round(result, 4)
