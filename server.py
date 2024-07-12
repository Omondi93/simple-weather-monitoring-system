import os
import cherrypy
import requests
from datetime import datetime


class WeatherMonitoringSystem:

    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_weather(self, city):
        api_key = 'YOUR OWN API KEY'  # Replace with your actual OpenWeatherMap API key
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if data.get('cod') != '200':
            return {'error': 'City not found'}

        weather_data = []
        for i in range(0, 40, 8):  # Fetch data for 5 days, each day at 12:00
            day_data = data['list'][i]
            weather_data.append({
                'date': datetime.fromtimestamp(day_data['dt']).strftime('%A'),
                'city': city,
                'temperature': day_data['main']['temp'],
                'humidity': day_data['main']['humidity'],
                'condition': day_data['weather'][0]['description']
            })

        return weather_data


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': current_dir,
            'tools.staticdir.index': 'index.html',
        },
        '/style.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(current_dir, 'style.css')
        },
        '/background-image.jpg': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(current_dir, 'noaa-99F4mC79j1I-unsplash.jpg')
        },
        '/download-icon.png': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(current_dir, 'weather app.png')
        }
    }
    cherrypy.quickstart(WeatherMonitoringSystem(), '/', config)
