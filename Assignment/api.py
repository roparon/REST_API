from flask import Flask, jsonify
import requests


app = Flask(__name__)



@app.route('/')
def home():
    return "<h1>Welcome to the world of api!</h1>"

API_URL = 'https://restcountries.com/v3.1/all'



#Checking the list of countries
@app.route('/countries')
def get_countries():
    response = requests.get(API_URL)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from API'}), 404
    return jsonify(response.json())

#Checking the name of a country
@app.route('/countries/<country_name>')
def get_country(country_name):
    response = requests.get(API_URL)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from API'}), 404
    countries = response.json()
    for country in countries:
        if country['name']['common'].lower() == country_name.lower():
            return jsonify(country)
    return jsonify({'error': 'Country not found'}), 404


#Checking the capital of a country
@app.route('/countries/capital/<capital_name>')
def get_country_by_capital(capital_name):
    response = requests.get(API_URL)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from API'}), 404
    countries = response.json()
    for country in countries:
        if 'capital' in country and capital_name.lower() in [cap.lower() for cap in country['capital']]:
            return jsonify(country)
    return jsonify({'error': 'Country not found'}), 404








if __name__ == '__main__':
    app.run(debug=True)