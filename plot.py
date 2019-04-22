import requests
from bs4 import BeautifulSoup as BS
import googlemaps
import geocoder
import webbrowser
import re
import nltk
import os


class Path:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.testdata = os.path.join(dirname, "\\Test\\TestData\\")


class Plot:
    def __init__(self, api):
        self.gmaps = googlemaps.Client(api)
        self.__api = api
        self.header_regex = re.compile('^h[1-6]$')
        self.link_regex = re.compile('a')
        self.headers = []
        self.links = []
        self.words_filter = nltk.corpus.stopwords.words('english')

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

    def read_url(self, url):
        r = requests.get(url)
        bs = BS(r.text, 'html.parser')
        [self.headers.append(i) for i in bs.find_all(self.header_regex)]
        for link in bs.find_all(self.link_regex):
            if link.has_attr('href'):
                self.links.append(link)

    def reset_attribs(self):
        self.headers = []
        self.links = []

    def filter_list(self, bs_list, words_filter):
        # bs_list = [header.text for header in plot.headers]
        output = []
        for header in bs_list:
            temp = []
            for word in header.split():

                if word not in words_filter:
                    temp.append(word)
            print(temp)
            output.append(" ".join(temp))
        return output

