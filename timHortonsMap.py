''' 
NAME: Janit Sriganeshaelankovan 
CREATED: November 6, 2018 - 14:15 (EDT)
GOAL: Tim Hortons Location on Map 
LAST UPDATE: July 14, 2019 - 16:26 (EDT)
'''

import os 
from bs4 import BeautifulSoup as soup
import requests 
import json
import folium 

CUR_DIR = ****** # current directory
API_KEY = ****** # Google API key 


os.chdir(CUR_DIR)


'''Webscrape all the Tim Hortons locations in Toronto'''
url = r'https://locations.timhortons.com/ca/on/toronto.html'
resp = requests.get(url)
html = resp.text
page_soup = soup(html, 'lxml')

location_street = [x.text for x in page_soup.find_all('span', {"class":"c-address-street-1"})]
location_postalcode = [x.text for x in page_soup.find_all('span', {"class":"c-address-postal-code"})]
location_number = [x.text for x in page_soup.find_all('span', {"class":"c-phone-number-span c-phone-main-number-span"})]
location_website = [link.get('href').replace('../..', r'https://locations.timhortons.com') for link in page_soup.find_all('a', {"class":"Teaser-titleLink"})]

street = list(zip(location_street, location_postalcode))

locations = {}
streets = []
for element1, element2 in (street):
    ele = element1.replace(',', ' ') + ' ' + element2.replace(',', '')    
    x = ele.replace('&#x20;', '')
    streets.append(x)
    
for idx, s in enumerate(streets):
    print(idx,s)
    locations[s] = [location_number[idx], location_website[idx]]


'''Get the geolocations of the locations using Google API'''
for key, value in locations.items():
    print(key)
    address = key
    endpoint = r"https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address, API_KEY)    
    response = requests.get(endpoint).json()    
    address_lat = response['results'][0]['geometry']['location']['lat']
    address_long = response['results'][0]['geometry']['location']['lng']
    locations[key].append(address_lat)    
    locations[key].append(address_long)

'''Output the location dictionary to txt file'''
with open('TimHortonsLocations.txt', 'w') as file:
     file.write(json.dumps(locations, indent=2))


'''Plot the locations on a map'''
folium_map = folium.Map(location= [43.6532, -79.3832],
                        zoom_start= 13,
                        tiles= "CartoDB dark_matter")    


for key, value in locations.items():
    lat = locations[key][2]
    long = locations[key][3] 

    icon = folium.features.CustomIcon('https://timhortons.com/ca/images/original-blend-product.png', 
                                      icon_size=(30,30))
    
    popup_text = """
                {}
                {}
                {}
                """
    popup_text = popup_text.format(key,
                               locations[key][0],
                               locations[key][1])
    popup = folium.Popup(popup_text, parse_html=True)
    folium.Marker([lat,long], popup=popup, icon=icon).add_to(folium_map)
    
folium_map.save("Toronto_TimHortons_07_14_2019.html")    












