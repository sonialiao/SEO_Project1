import requests
import datetime
import json

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
    BASE_URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=imperial"
    response = requests.get(BASE_URL).json()
    days = response.get('list')

    forecast = []
    for day in days:
        w = Weather(date = datetime.datetime.fromtimestamp(day.get('dt')),
            details = (details := day.get('main')),
            temp = details.get('temp'),
            weather = (weather := day.get('weather')),
            description=weather[0].get('description'))

        forecast.append(w)
    
    return forecast

def display_forecast():

    city = input("Enter your city: ")
    forecast = get_weather(city)
    

    for f in forecast:
        print(f)
        print()
        print()
        print()

display_forecast() 