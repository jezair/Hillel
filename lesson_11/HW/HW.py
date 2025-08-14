import requests

def get_rate(from_currency, to_currency):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency,
        "apikey": API
    }

    response = requests.get(url, params=params)
    data = response.json()
    try:
        rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        return rate
    except KeyError:
        print("Ошибка: не удалось получить курс")
        return None


API = "V58WIZKUTUB6X1DK"

class Price():
    def __init__(self, value, currency):
        self.value = value
        self.currency = currency

    def __add__(self, other):
        if self.currency == other.currency:
            result_in_same_curr = other.value + self.value
            return Price(result_in_same_curr, self.currency)
        else:
            self_in_chf = self.convert_to_chf()
            other_in_chf = other.convert_to_chf()

            result_in_chf = self_in_chf + other_in_chf
            coefficient = get_rate("CHF", self.currency)

            result_in_old_curr = result_in_chf * coefficient
            return Price(result_in_old_curr, self.currency)

    def __sub__(self, other):
        if self.currency == other.currency:
            result_in_same_curr = other.value - self.value
            return Price(result_in_same_curr, self.currency)
        else:
            self_in_chf = self.convert_to_chf()
            other_in_chf = other.convert_to_chf()

            result_in_chf = self_in_chf - other_in_chf
            coefficient = get_rate("CHF", self.currency)

            result_in_old_curr = result_in_chf * coefficient
            return Price(result_in_old_curr, self.currency)

    def __str__(self):
        return f"{self.value:.2f} {self.currency}"

    def convert_to_chf(self):
        coefficient = get_rate(self.currency, "CHF")
        return self.value * coefficient

    def convert_from_chf(self):
        coefficient = get_rate("CHF", self.currency)
        return self.value * coefficient


a = Price(100, "USD")
b = Price(150, "UAH")
c = Price(150, "UAH")

r = a+b
print(r)
