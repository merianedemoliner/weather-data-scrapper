#https://www.wunderground.com/weather/br/nova-santa-rita
import requests, bs4
cities = ['nova-santa-rita', 'novo-hamburgo', 'parobe', 'tres-coroas', 'rolante', 'caraa']
temperature_css_selector = '.current-temp > lib-display-unit:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
humidity_css_selector = ' .wu-unit-humidity > span:nth-child(1)'
clouds_css_selector = 'span.wx-value:nth-child(1)'
precipitation_css_selector = '.additional-conditions > div:nth-child(2) > div:nth-child(1) > div:nth-child(6) > div:nth-child(2) > lib-display-unit:nth-child(1) > span:nth-child(1) > span:nth-child(1)'



for city in cities:
    html_page = requests.get('https://www.wunderground.com/weather/br/' + city)
    html_parsed = bs4.BeautifulSoup(html_page.text, 'html.parser')
    temperature_elements = html_parsed.select(temperature_css_selector)
    humidity_elements = html_parsed.select(humidity_css_selector)
    clouds_elements = html_parsed.select(clouds_css_selector)
    precipitation_elements = html_parsed.select(precipitation_css_selector)    
    
    print("City: " + city +  "\tTemperature: " + temperature_elements[0].text + "F\tHumidity: " + humidity_elements[0].text + "%\tClouds: " + clouds_elements[0].text + "\tPrecipitation: " + precipitation_elements[0].text)
