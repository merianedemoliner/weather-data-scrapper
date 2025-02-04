import requests, bs4
from datetime import datetime
from pytz import timezone
from mysql.connector import MySQLConnection, Error
from weatherdb_config import read_db_config

def convert_fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

def insert_data_by_city(city, temperature_c, temperature_f, humidity, clouds, precipitation, datetime):
    insert_command = "INSERT INTO waether_history(city,temperature_celsius,temperature_fahrenheit,humidity,clouds,precipitation, datetime) " \
            "VALUES(%s,%s,%s,%s,%s,%s,%s)"
    args = (city, temperature_c, temperature_f, humidity, clouds, precipitation, datetime)
 
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(insert_command, args)
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

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
    temperature_c = str(convert_fahrenheit_to_celsius(float(temperature_f.text)))
    humidity = html_parsed.select_one(humidity_css_selector)
    clouds = html_parsed.select_one(clouds_css_selector)
    precipitation = html_parsed.select_one(precipitation_css_selector)    
    datetime_brazilian = datetime.now(timezone('America/Sao_Paulo'))

    print("inserting data for " + city)
    insert_data_by_city(city, temperature_c, temperature_f.text, humidity.text, clouds.text, precipitation.text, datetime_brazilian)
