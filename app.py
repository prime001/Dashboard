import requests
import configparser, os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def dashboard_setup():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def render_dashboard():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data['main']["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"]["main"]
    location = data["name"]

    return render_template('dashboard.html',
                           location=location, temp=temp, feels_like=feels_like, weather=weather)

if __name__ == '__main__':
    app.run(port='5001')

def get_api_key():
    config = configparser.RawConfigParser()
    config.read_file(open('config.ini'))
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'.format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()



print(get_weather_results("59105", get_api_key()))