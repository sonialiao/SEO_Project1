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

    forecast = []
    for day in days:
        w = Weather(date=datetime.datetime.fromtimestamp(day.get('dt')),
                    details=(details := day.get('main')),
                    temp=details.get('temp'),
                    weather=(weather := day.get('weather')),
                    description=weather[0].get('description'))

        forecast.append(w)

    return forecast


def display_forecast(city):
    forecast = get_weather(city)
    for f in forecast:
        print(f)
        print()


def display_history():
    hist = query_history('db1.db')
    for h in hist:
        print(f"{h[0]} | {h[1]}")


def weather_query():
    city = input("Enter your city: ")
    display_forecast(city)
    insert_history('db1.db', city)


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
                break
            case 'w' | 'weather':
                weather_query()
                print("===")
            case 'h' | 'history':
                display_history()
                print("===")
            case _:
                print("Not a supported request. Please try again.")

    # before exiting program, clear history
    delete_database(db_name)


if __name__ == '__main__':
    main()
