import requests, bs4
from mysql.connector import MySQLConnection, Error
from weatherdb_config import read_db_config

def convert_fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

# target cities
cities = ['nova-santa-rita', 'canoas', 'novo-hamburgo', 'sao-leopoldo', 'parobe', 'taquara', 'tres-coroas', 'igrejinha', 'rolante', 'riozinho', 'caraa', 'santo-antonio-da-patrulha']

# css selectors, relevant for scrapping
temperature_css_selector = '.current-temp > lib-display-unit:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
humidity_css_selector = ' .wu-unit-humidity > span:nth-child(1)'
clouds_css_selector = 'span.wx-value:nth-child(1)'
precipitation_css_selector = '.additional-conditions > div:nth-child(2) > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > lib-display-unit:nth-child(1) > span:nth-child(1) > span:nth-child(1)'

for city in cities:
    html_page = requests.get('https://www.wunderground.com/weather/br/' + city)
    html_parsed = bs4.BeautifulSoup(html_page.text, 'html.parser')
    temperature_f = html_parsed.select_one(temperature_css_selector)
    temperature_c = convert_fahrenheit_to_celsius(float(temperature_f.text))
    humidity = html_parsed.select_one(humidity_css_selector)
    clouds = html_parsed.select_one(clouds_css_selector)
    precipitation = html_parsed.select_one(precipitation_css_selector)    
    
    print("City: " + city +  "\tTemperature: " + temperature_f.text + "F\tTemperature(C): " + str(temperature_c) + "C\tHumidity: " + humidity.text + "%\tClouds: " + clouds.text + "\tPrecipitation: " + precipitation.text)

# def connect():
#     """ Connect to MySQL database """
#     connection = None
#     try:
#         connection = mysql.connector.connect(host='weather-database.c43aqgloj5aq.sa-east-1.rds.amazonaws.com',
#                                              database='weatherdb',
#                                              user='admin',
#                                              password='meridoutorado')
#         if connection.is_connected():
#             print('Connected to MySQL database')
 
#     except Error as e:
#         print(e)
 
#     finally:
#         if connection is not None and connection.is_connected():
#             connection.close()


# def insert_data_by_city(city, temperature_c, temperature_f):
#     query = "INSERT INTO waether_history(city,teme) " \
#             "VALUES(%s,%s)"
#     args = (title, isbn)
 
#     try:
#         db_config = read_db_config()
#         conn = MySQLConnection(**db_config)
 
#         cursor = conn.cursor()
#         cursor.execute(query, args)
 
#         if cursor.lastrowid:
#             print('last insert id', cursor.lastrowid)
#         else:
#             print('last insert id not found')
 
#         conn.commit()
#     except Error as error:
#         print(error)
 
#     finally:
#         cursor.close()
#         conn.close()