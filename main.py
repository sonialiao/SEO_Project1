import requests
import datetime
import json
from dbscript import create_database, delete_database, insert_history, query_history    # noqa


class Weather:
    def __init__(self, date, details, temp, weather, description):
        self.date = date
        self.details = details
        self.temp = temp
        self.weather = weather
        self.description = description

    def get_date(self):
        return self.date

    def get_details(self):
        return self.details

    def get_temp(self):
        return self.details

    def get_weather(self):
        return self.weather

    def get_description(self):
        return self.description

    def __str__(self):
        return f'[{self.date:%H:%M}] {self.temp}F° ({self.description})'


API_KEY = "6fbacf036c067a7f025361d3f16b32f4"


def get_weather(city):
    BASE_URL = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial'  # noqa
    response = requests.get(BASE_URL).json()
    days = response.get('list')

    if days is None:
        print("Error occurred while fetching weather from API")
        return

    forecast = []
    for day in days:
        w = Weather(date=datetime.datetime.fromtimestamp(day.get('dt')),
                    details=(details := day.get('main')),
                    temp=details.get('temp'),
                    weather=(weather := day.get('weather')),
                    description=weather[0].get('description'))

        forecast.append(w)

    return forecast


def display_forecast(forecast, bars):

    for i in range(len(forecast)):
        entry = forecast[i]
        char_bar = bars[i]
        print_str = f'[{entry.date:%H:%M}] {char_bar}  {entry.temp}°F ({entry.description})'   # noqa
        print(print_str)


def forecast_bars(forecast):
    temperatures = list(map(lambda w: (w.temp), forecast))
    min_temp = min(temperatures)
    max_temp = max(temperatures)

    def min_max_scale(orig):
        return (orig-min_temp) / (max_temp-min_temp)

    scaled_temps = list(map(min_max_scale, temperatures))
    adjust = 50

    def draw_bar(value, adjust, char="❚"):
        return max(int(value * adjust), 1) * char

    bars = list(map(lambda s: draw_bar(s, adjust), scaled_temps))

    return bars


def display_history(db_name):
    hist = query_history(db_name)
    for h in hist:
        print(f"{h[0]} | {h[1]} | {h[2]}")
    return 0


def weather_query(db_name):

    return_cond = False
    while not return_cond:
        city = input("Enter your city: ")

        if city == '<' or city == "quit":
            return_cond = True
            continue

        forecast = get_weather(city)
        if forecast is None:
            # fetched nothing, prompt again
            continue

        bars_for_graph = forecast_bars(forecast)
        display_forecast(forecast, bars_for_graph)

        weather_hist = f"{forecast[0].temp}°F ({forecast[0].description})"
        insert_history(db_name, city, weather_hist)


def main():

    # Set up
    quit_cond = False
    db_name = 'db1.db'
    create_database(db_name)

    # loop for various input queries
    while not quit_cond:
        mode = input("Select Mode: ")
        match mode:
            case 'q' | 'quit':
                quit_cond = True
            case 'w' | 'weather':
                weather_query(db_name)
                print("===")
            case 'h' | 'history':
                display_history(db_name)
                print("===")
            case _:
                print("Not a supported request. Please try again.")

    # before exiting program, clear history
    delete_database(db_name)


if __name__ == '__main__':
    main()
