
import requests
import random
import os 
import json

def weather_forecast(city):
    # If the recognized city is blank, set default to "Kathmandu"
    city = city if city.strip() else "Kathmandu"

    base_url = 'https://api.openweathermap.org/data/2.5/weather?'
    api_key = os.getenv("WEATHER_API_KEY")

    if api_key is None:
        print("API key is missing or invalid.")
        return (f"Error: API key is missing or invalid. Please set a valid API key.", None, None)

    url = f"{base_url}q={city}&appid={api_key}"
    response = requests.get(url)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return (f"Error: Could not retrieve weather data for {city}. Please try again later.", None, None)

    if response.status_code == 200:
        # Save JSON response to a file
        file_path = 'data_archive/weather_data.json'
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(response.json(), json_file, ensure_ascii=False, indent=4)

        # Load JSON file
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        description = data.get("weather", [{}])[0].get("description")

        # Extracting temperature (Kelvin to Celsius)
        temperature = data.get("main", {}).get("temp")
        if temperature is not None:
            temperature -= 273.15
            temperature = round(temperature, 2)
        else:
            temperature = "N/A"

        return (city, description, temperature)
    else:
        print(f"Error: {response.status_code}. Could not retrieve weather data for {city}.")
        return (f"Error: Could not retrieve weather data for {city}. Please try again later.", None, None)