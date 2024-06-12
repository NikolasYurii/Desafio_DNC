import requests
import pandas as pd
from sqlalchemy import create_engine

# Configurações das APIs
WEATHER_API_KEY = '82ac8190afb1d7e23fa78650ac6dde28'
TRAFFIC_API_KEY = 'AIzaSyCB2LmnHl4zANdBtWzOUM2RD6k919mzp3k'
DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/DesafioDNCbd'

# Função para obter dados de clima
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    response = requests.get(url)
    data = response.json()
    temperature_kelvin = data.get('main', {}).get('temp')
    temperature_celsius = temperature_kelvin - 273.15 if temperature_kelvin is not None else None
    timestamp = pd.to_datetime(data.get('dt'), unit='s').strftime('%d/%m/%Y')
    return {
        'city': city,
        'temperature': temperature_celsius,
        'humidity': data.get('main', {}).get('humidity'),
        'weather': data.get('weather', [{}])[0].get('description'),
        'timestamp': timestamp
    }

# Função para obter dados de trânsito
def get_traffic_data(origin, destination):
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={TRAFFIC_API_KEY}'
    response = requests.get(url)
    data = response.json()
    route = data['routes'][0]['legs'][0]
    timestamp = pd.Timestamp.now().strftime('%d/%m/%Y')
    return {
        'origin': origin,
        'destination': destination,
        'distance': route['distance']['value'],
        'duration': route['duration']['value'],
        'timestamp': timestamp
    }

# Conexão ao banco de dados
engine = create_engine(DATABASE_URI)

# Obtenção e armazenamento dos dados de clima
cities = ['Sao Paulo', 'Rio de Janeiro']
weather_data = [get_weather_data(city) for city in cities]
weather_df = pd.DataFrame(weather_data)
weather_df.to_sql('clima', engine, if_exists='replace', index=False)

# Obtenção e armazenamento dos dados de trânsito
routes = [('Sao Paulo', 'Rio de Janeiro')]
traffic_data = [get_traffic_data(origin, destination) for origin, destination in routes]
traffic_df = pd.DataFrame(traffic_data)
traffic_df.to_sql('traffic', engine, if_exists='replace', index=False)

print("Dados de clima e trânsito carregados no banco de dados.")

# Exemplo de adição de instruções print para depuração

# Após a chamada da API de clima
print("Dados de clima:")
print(weather_data)

# Após a chamada da API de tráfego
print("Dados de tráfego:")
print(traffic_data)
