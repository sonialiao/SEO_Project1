import requests
import datetime
import json
import os
from dbscript import create_database, delete_database, insert_history, query_history    # noqa


class Weather:      # weather class, contains data of the forecast
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


API_KEY = os.getenv('key')      # gets your api key


def get_weather(city):      # pulls all of the information from the response
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


def display_forecast(forecast):     # helper method to print out the forecast
    for f in forecast:
        print(f)
        print()


def display_history(db_name):       # displays the database
    hist = query_history(db_name)
    for h in hist:
        print(f"{h[0]} | {h[1]} | {h[2]}")
    return 0


def weather_query(db_name):        # inserts the information into the database

    return_cond = False
    while not return_cond:
        city = input("Enter your city: ")

        if city == '<':
            return_cond = True
            continue

        forecast = get_weather(city)
        display_forecast(forecast)

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
