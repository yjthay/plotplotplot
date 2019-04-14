import requests
from bs4 import BeautifulSoup as BS
import googlemaps
import geocoder
import webbrowser
import re


class Plot:
    def __init__(self, api):
        self.gmaps = googlemaps.Client(api)
        self.__api = api
        self.header_regex = re.compile('^h[1-6]$')

    def find_place(self, locations, location_supplement=None):
        if not isinstance(locations, list):
            locations = locations.split("\n")
        if location_supplement is not None:
            locations = [location + "," + location_supplement for location in locations]
        output = dict()
        for location in locations:
            print('Looking for location: {}'.format(location))
            details = geocoder.google(location, key=self.__api).json
            if details is not None and details['status'] == 'OK':
                temp = self.gmaps.place(details['place'])
                if temp['status'] == 'OK':
                    x = dict()
                    place_details = temp['result']
                    x['location'] = place_details['geometry']['location']
                    x['url'] = place_details['url']
                    output[place_details['name']] = x
                    webbrowser.open(place_details['url'])
            else:
                print("Unable to find {}".format(location))
        return output

    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.readlines()

    def read_url(self, url):
        r = requests.get(url)
        bs = BS(r.text, 'html.parser')
        headers = bs.find_all(self.header_regex)
        return headers
