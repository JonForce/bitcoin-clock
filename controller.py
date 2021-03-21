import requests
from datetime import datetime
from datetime import timedelta
from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtCore import QThread


class Controller:

    UPDATE_FREQUENCY = 2000 # millis
    STORE_BTC_PRICE_FREQUENCY = 60 # seconds
    OLDEST_ALLOWED_PRICE = 60*60*24 # seconds
    GIF_DURATION = 60 # seconds
    prices = []

    def __init__(self, gif_manager, clock_window):
        self.gif_manager = gif_manager
        self.clock_window = clock_window
        self.gif_start_time = datetime.now()

        self.timer = QTimer()
        self.timer.timeout.connect(self._refresh_timer)
        self.timer.start(self.UPDATE_FREQUENCY)

        self._refresh_timer()

    def _refresh_timer(self):
        print("Refresh")
        self.timer.start(self.UPDATE_FREQUENCY)
        self._update_btc_price()
        text = f"${self.btc_price['str']} ({round(self._percent_change()*100, ndigits=2)}%)"
        self.clock_window.set_display_text(text, "green" if self._percent_change() >= 0 else "red")

        if self._gif_duration() > self.GIF_DURATION:
            query = "to the moon" if self._percent_change() >= 0 else "diamond hands"
            self.clock_window.update_gif(self.gif_manager.grab_gif(query))
            self.gif_start_time = datetime.now()
            print("Updating gif")


    def _update_btc_price(self):
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        price = {
            "time": datetime.now(),
            "float": float(response.json()["bpi"]["USD"]["rate"].replace(",", "")),
            "str": response.json()["bpi"]["USD"]["rate"].split(".")[0]
        }
        self.btc_price = price
        if len(self.prices) == 0 or self._elapsed(self.prices[-1]['time']) > self.STORE_BTC_PRICE_FREQUENCY:
            self.prices.append(price)
            print(f"Added new btc price, length = {len(self.prices)}")

        i = 0
        while True:
            oldest_price = self.prices[0]
            if oldest_price is None or i >= len(self.prices):
                break
            elif self._elapsed(oldest_price['time']) > self.OLDEST_ALLOWED_PRICE:
                self.prices.remove(oldest_price)
                print(f"Removed btc price, age : {self._elapsed(oldest_price['time']).seconds}")
            else:
                i += 1

    # Default to the percent change in the last hour
    def _percent_change(self, duration=60*60):
        closest_price = None
        target_time = datetime.now() - timedelta(seconds=duration)
        for price in self.prices:
            if closest_price is None or abs((price["time"] - target_time).seconds) < abs((closest_price["time"] - target_time).seconds):
                closest_price = price
        # % increase = Increase ÷ Original Number × 100.
        return (self.btc_price["float"] - closest_price["float"]) / closest_price["float"]

    def _elapsed(self, old_time):
        return (datetime.now() - old_time).seconds

    def _gif_duration(self):
            return self._elapsed(self.gif_start_time)