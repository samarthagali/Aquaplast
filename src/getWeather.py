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
    
def get_daily_forecast(latitude, longitude, api_key):
    count = 6
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={latitude}&lon={longitude}&cnt={count}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any errors in the response
        forecast = response.json()
        return forecast
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def convert_timestamp_to_local_time(timestamp, timezone):
    utc_time = datetime.utcfromtimestamp(timestamp)
    local_time = utc_time + timedelta(seconds=timezone)
    return local_time.strftime('%H:%M')

def create_html_page(weather_data,forecast_data):
    sunrise_time = convert_timestamp_to_local_time(weather_data['sys']['sunrise'], weather_data['timezone'])
    sunset_time = convert_timestamp_to_local_time(weather_data['sys']['sunset'], weather_data['timezone'])
    img_link = "{{ url_for('static', filename='public/AquaPlast_Logo.jpeg') }}"
    css_link = "{{ url_for('static', filename='styles/environment.css') }}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistics on Plastic Levels</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Phudu:wght@500&family=Special+Elite&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{css_link}">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5 mb-3">Weather Forecast</h1>
            <div class="back" id="bACKText"><a href="{{url_for('predict_datapoint')}}"><img class="logo" src="{img_link}" alt="logo"></a></div>
            <div class="row">
                <div class="col-md-6">
                    <h2>Location: {weather_data['name']}    , {weather_data['sys']['country']}</h2>
                    <h3>Current Weather: {weather_data['weather'][0]['description']}</h3>
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
        <h2>Weather Forecast</h2>
        <div class="div1">

    """
    # Iterate through the forecast data
    for day_data in forecast_data['list']:

        date = day_data['dt']
        date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
        max_temp = day_data['temp']['max']
        min_temp = day_data['temp']['min']
        weather_icon = day_data['weather'][0]['icon']
        weather_description = day_data['weather'][0]['description']

        print(date,max_temp,min_temp,weather_icon,weather_description)
        # Create an HTML card for each day
        html_card = f"""
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
            <p>Date: {date}</p>
            <p>Max Temp: {max_temp-273.15:.1f}°C</p>
            <p>Min Temp: {min_temp-273.15:.1f}°C</p>
            <img src="https://openweathermap.org/img/wn/{weather_icon}@2x.png" alt="{weather_description}">
            <p>Weather: {weather_description}</p>
        </div>
        """

        # Append the card to the HTML document
        html_content += html_card

    # Close the HTML document
    html_content += "</div></body></html>"




    return html_content

def get_data(geotag):
    # Replace these values with your actual latitude, longitude, and API key
    df = pd.read_csv(geotag)

    # weather_json = '{"coord": {"lon": 106.6944, "lat": 10.8959}, "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02n"}], "base": "stations", "main": {"temp": 302.18, "feels_like": 309.18, "temp_min": 302.18, "temp_max": 302.18, "pressure": 1012, "humidity": 89}, "visibility": 10000, "wind": {"speed": 4.12, "deg": 240}, "clouds": {"all": 20}, "dt": 1691246551, "sys": {"type": 1, "id": 9314, "country": "VN", "sunrise": 1691188927, "sunset": 1691234186}, "timezone": 25200, "id": 1580578, "name": "Ho Chi Minh City", "cod": 200}'
    # forecast_json = "{'city': {'id': 1580578, 'name': 'Ho Chi Minh City', 'coord': {'lon': 106.6941, 'lat': 10.8959}, 'country': 'VN', 'population': 0, 'timezone': 25200}, 'cod': '200', 'message': 3.8041599, 'cnt': 5, 'list': [{'dt': 1693800000, 'sunrise': 1693781014, 'sunset': 1693825312, 'temp': {'day': 302.4, 'min': 298.56, 'max': 303.47, 'night': 298.84, 'eve': 301.73, 'morn': 298.77}, 'feels_like': {'day': 307.69, 'night': 299.84, 'eve': 306.56, 'morn': 299.92}, 'pressure': 1006, 'humidity': 76, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'speed': 6.58, 'deg': 245, 'gust': 10.38, 'clouds': 97, 'pop': 1, 'rain': 13.64}, {'dt': 1693886400, 'sunrise': 1693867412, 'sunset': 1693911674, 'temp': {'day': 303.51, 'min': 298.23, 'max': 303.65, 'night': 298.36, 'eve': 299.38, 'morn': 298.26}, 'feels_like': {'day': 309.62, 'night': 299.34, 'eve': 299.38, 'morn': 299.28}, 'pressure': 1007, 'humidity': 72, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'speed': 7.22, 'deg': 222, 'gust': 13.31, 'clouds': 99, 'pop': 1, 'rain': 12.62}, {'dt': 1693972800, 'sunrise': 1693953809, 'sunset': 1693998036, 'temp': {'day': 300.21, 'min': 297.95, 'max': 302.38, 'night': 298.4, 'eve': 301.06, 'morn': 298.19}, 'feels_like': {'day': 303.42, 'night': 299.41, 'eve': 305.17, 'morn': 299.15}, 'pressure': 1010, 'humidity': 84, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'speed': 6.3, 'deg': 257, 'gust': 11.22, 'clouds': 100, 'pop': 1, 'rain': 7.74}, {'dt': 1694059200, 'sunrise': 1694040206, 'sunset': 1694084398, 'temp': {'day': 302.32, 'min': 297.53, 'max': 303.68, 'night': 299.29, 'eve': 303.68, 'morn': 297.53}, 'feels_like': {'day': 306.85, 'night': 299.29, 'eve': 309.24, 'morn': 298.48}, 'pressure': 1010, 'humidity': 73, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'speed': 2.88, 'deg': 287, 'gust': 5.9, 'clouds': 100, 'pop': 0.99, 'rain': 12.34}, {'dt': 1694145600, 'sunrise': 1694126603, 'sunset': 1694170760, 'temp': {'day': 302.04, 'min': 297.79, 'max': 304.24, 'night': 299.51, 'eve': 303.05, 'morn': 297.79}, 'feels_like': {'day': 306.77, 'night': 299.51, 'eve': 308.67, 'morn': 298.76}, 'pressure': 1010, 'humidity': 76, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'speed': 4.17, 'deg': 310, 'gust': 8.12, 'clouds': 100, 'pop': 0.97, 'rain': 13.2}]}"

    latitude = df['Latitude'].mean()
    longitude = df['Longitude'].mean()
    api_key = "b84bb131f7e632811e1a16d170bcd068"
    
    weather_data = get_weather_data(latitude, longitude, api_key)
    forecast = get_daily_forecast(latitude, longitude, api_key)
    # weather_data = json.loads(weather_json)
    # forecast = json.loads(forecast_json)

    # print("Forecast Data:")
    # print(forecast)
    if weather_data and forecast:
        print("Weather Data:")
        print(weather_data)
        html_page_content = create_html_page(weather_data,forecast)
        with open("templates/environment.html", "w",encoding='utf-8') as f:
            f.write(html_page_content)
        print("Weather data successfully retrieved!")
    else:
        print("Failed to retrieve weather data.")
        
