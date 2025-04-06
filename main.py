import requests
API_KEY = '81bdb230e5e5201078981ef3d6493562'  # Replace with your actual API key

def get_weather(city):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return {
            'city': city,
            'weather': weather,
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed
        }
    else:
        print(f"Error: {response.status_code}, Message: {response.json()}")
        return None

weather_place_mapping = {
    'clear sky': ['park', 'outdoor cafe', 'zoo'],
    'few clouds': ['park', 'outdoor cafe'],
    'scattered clouds': ['museum', 'art gallery'],
    'broken clouds': ['museum', 'art gallery'],
    'shower rain': ['museum', 'indoor shopping mall'],
    'rain': ['museum', 'indoor shopping mall'],
    'thunderstorm': ['indoor shopping mall', 'library'],
    'snow': ['library', 'coffee shop'],
    'mist': ['library', 'coffee shop']
}

def recommend_places(weather_condition):
    recommendations = weather_place_mapping.get(weather_condition.lower(), [])
    if recommendations:
        print("Based on the current weather, you might enjoy visiting:")
        for place in recommendations:
            print(f"- {place.title()}")
    else:
        print("No specific recommendations for this weather condition.")


if __name__ == '__main__':
    city = input('Enter the city name: ')
    weather_data = get_weather(city)
    if weather_data:
        print(f"Weather in {weather_data['city']}:")
        print(f"  Condition: {weather_data['weather']}")
        print(f"  Temperature: {weather_data['temperature']}°C")
        print(f"  Humidity: {weather_data['humidity']}%")
        print(f"  Wind Speed: {weather_data['wind_speed']} m/s")
        recommend_places(weather_data['weather'])
    else:
        print('Failed to retrieve weather data.')