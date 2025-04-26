from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)
API_KEY = "cdbbb6064097f4d9df96b81d563be035"  # Sostituisci con la tua chiave API

def get_current_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + API_KEY + "&q=" + city + "&units=metric&lang=it"
    response = requests.get(complete_url)
    data = response.json()
    return data

def get_forecast(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "appid=" + API_KEY + "&q=" + city + "&units=metric&lang=it"
    response = requests.get(complete_url)
    data = response.json()
    return data

@app.route('/weather/<city>')
def weather(city):
    current_weather_data = get_current_weather(city)
    forecast_data = get_forecast(city)

    if current_weather_data["cod"] == 200 and forecast_data["cod"] == "200":
        return jsonify({
            'current': {
                'city': current_weather_data.get('name'),
                'temp': current_weather_data['main'].get('temp'),
                'description': current_weather_data['weather'][0].get('description').capitalize(),
                'humidity': current_weather_data['main'].get('humidity'),
                'wind': current_weather_data['wind'].get('speed')
            },
            'forecast': process_forecast_data(forecast_data['list'])
        })
    else:
        return jsonify({'error': 'Impossibile recuperare i dati meteo per la città specificata.'}), 404

def process_forecast_data(forecast_list):
    daily_forecast = {}
    for item in forecast_list:
        date = item["dt_txt"].split(" ")[0]
        time = item["dt_txt"].split(" ")[1]
        if date not in daily_forecast:
            daily_forecast[date] = {
                "min_temp": float('inf'),
                "max_temp": float('-inf'),
                "conditions": [],
                "main_condition_icon": None
            }
        daily_forecast[date]["min_temp"] = min(daily_forecast[date]["min_temp"], item["main"]["temp_min"])
        daily_forecast[date]["max_temp"] = max(daily_forecast[date]["max_temp"], item["main"]["temp_max"])
        daily_forecast[date]["conditions"].append(item["weather"][0]["description"])
        if time == "12:00:00":
            daily_forecast[date]["main_condition_icon"] = item["weather"][0]["icon"]

    icon_map = {
        "01d": "Sole", "01n": "Luna piena", "02d": "Nuvole sparse", "02n": "Poche nuvole",
        "03d": "Nuvole sparse", "03n": "Nuvole sparse", "04d": "Nuvoloso", "04n": "Nuvoloso",
        "09d": "Pioggia leggera", "09n": "Pioggia leggera", "10d": "Pioggia", "10n": "Pioggia",
        "11d": "Temporale", "11n": "Temporale", "13d": "Neve", "13n": "Neve", "50d": "Nebbia", "50n": "Nebbia",
    }

    formatted_forecast = []
    for date, data in daily_forecast.items():
        conditions_str = ", ".join(set(data["conditions"]))
        icon_description = icon_map.get(data["main_condition_icon"], "Sconosciuto")
        formatted_forecast.append({
            'date': datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y'),
            'icon': icon_description,
            'min_temp': f"{data['min_temp']:.1f}",
            'max_temp': f"{data['max_temp']:.1f}",
            'conditions': conditions_str.capitalize()
        })
    return formatted_forecast

if __name__ == '__main__':
    app.run(debug=True)