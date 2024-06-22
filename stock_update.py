import requests
from twilio.rest import Client

class Stock:

    API_KEY = "..."
    COUNTRY = "United States"
    URL_PREFIX = "https://api.twelvedata.com/"

    @classmethod
    def set_market_state(cls, s1, s2):
        cls.is_open = (s1.market_state and s2.market_state)

    @classmethod
    def set_day_change(cls, s1, s2):
        cls.day_change = round(((s1.portfolio_percentage * s1.percent_change) + (s2.portfolio_percentage * s2.percent_change)), 2)

    @classmethod
    def set_day_type(cls):
        if(cls.day_change >= 0.00):

            if(cls.day_change >= 1.00):
                cls.day_type = " Great day for you! "

            else:
                cls.day_type = " Good day for you! "

        elif(cls.day_change < 0.00):
            cls.day_type = " Good day for buying! "

    @classmethod
    def set_day_emoji(cls):
        if(cls.day_change >= 0.00):
            cls.day_emoji = "\U0001F4C8"

        elif(cls.day_change < 0.00):
            cls.day_emoji = "\U0001F4C9"

    @classmethod
    def set_all(cls, s1, s2):
        cls.set_market_state(s1, s2)
        cls.set_day_change(s1, s2)
        cls.set_day_type()
        cls.set_day_emoji()
        

    def __init__(self, ticker, percent):
        self.TICKER = ticker
        self.portfolio_percentage = round((percent / 100), 4)
        self.data = self.get_stock_data()
        self.open = self.data['open']
        self.close = self.data['close']
        self.percent_change = float(self.data['percent_change'])
        self.market_state = self.data['is_market_open']
        self.sign = "+" if (self.percent_change >= 0.0) else ""
        self.emoji = "\U00002705" if (self.sign) else "\U000026D4"
    
    def get_stock_data(self):
        url = f"{Stock.URL_PREFIX}quote?symbol={self.TICKER}&apikey={Stock.API_KEY}"
        return requests.get(url).json()
    

SCHD = Stock("SCHD", 25.99)
VOO = Stock("VOO", 74.01)
Stock.set_all(VOO, SCHD)


account_sid = '...'
auth_token = '...'
client = Client(account_sid, auth_token)

formatted_msg = emoji + dayType + emoji + \
    "\n\n" + VOO.emoji + " VOO: " + "(" + VOO.sign + str(VOO.percent_change) + "%)\n" + \
    "-------\n" + "Open: $" + VOO.open[:-3] + "\nClose: $" \
    + VOO.close[:-3] + "\n\n" + SCHD.emoji + " SCHD: " + "(" + SCHD.sign + \
    str(SCHD.percent_change) + "%)\n" + "-------\n" + "Open: $" + \
    SCHD.open[:-3] + "\nClose: $" + SCHD.close[:-3]

message = client.messages \
                .create(
                     body= formatted_msg,
                     from_='...',
                     to='...'
                 )


