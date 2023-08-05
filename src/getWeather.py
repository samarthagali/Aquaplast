import requests
import pandas as pd
import json
from datetime import datetime, timedelta

def get_weather_data(latitude, longitude, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any errors in the response
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def convert_timestamp_to_local_time(timestamp, timezone):
    utc_time = datetime.utcfromtimestamp(timestamp)
    local_time = utc_time + timedelta(seconds=timezone)
    return local_time.strftime('%H:%M')

def create_html_page(weather_data):
    sunrise_time = convert_timestamp_to_local_time(weather_data['sys']['sunrise'], weather_data['timezone'])
    sunset_time = convert_timestamp_to_local_time(weather_data['sys']['sunset'], weather_data['timezone'])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Forecast</title>
        <!-- Include Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5 mb-3">Weather Forecast</h1>
            <div class="row">
                <div class="col-md-6">
                    <h2>Location: {weather_data['name']}    , {weather_data['sys']['country']}</h2>
                    <h3>Weather: {weather_data['weather'][0]['description']}</h3>
                    <p>Temperature: {(weather_data['main']['temp']-273.15):.1f}&deg;C</p>
                    <p>Feels like: {(weather_data['main']['feels_like']-273.15):.1f}&deg;C</p>
                    <p>Humidity: {weather_data['main']['humidity']}%</p>
                    <p>Wind Speed: {weather_data['wind']['speed']} meter/sec</p>
                    <p>Cloudiness: {weather_data['clouds']['all']} %</p>
                    <p>Sunrise Time: {sunrise_time}</p>
                    <p>Sunset Time: {sunset_time}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def get_data(geotag):
    # Replace these values with your actual latitude, longitude, and API key
    df = pd.read_csv(geotag)

    # json_string = '{"coord": {"lon": 106.6944, "lat": 10.8959}, "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02n"}], "base": "stations", "main": {"temp": 302.18, "feels_like": 309.18, "temp_min": 302.18, "temp_max": 302.18, "pressure": 1012, "humidity": 89}, "visibility": 10000, "wind": {"speed": 4.12, "deg": 240}, "clouds": {"all": 20}, "dt": 1691246551, "sys": {"type": 1, "id": 9314, "country": "VN", "sunrise": 1691188927, "sunset": 1691234186}, "timezone": 25200, "id": 1580578, "name": "Ho Chi Minh City", "cod": 200}'
    
    latitude = df['Latitude'].mean()
    longitude = df['Longitude'].mean()
    api_key = "b84bb131f7e632811e1a16d170bcd068"
    
    weather_data = get_weather_data(latitude, longitude, api_key)
    # weather_data = json.loads(json_string)
    
    if weather_data:
        print("Weather Data:")
        print(weather_data)
        html_page_content = create_html_page(weather_data)
        with open("templates/environment.html", "w") as f:
            f.write(html_page_content)
    else:
        print("Failed to retrieve weather data.")
        
