from unittest import TestCase
from unittest import mock
from plot import Plot
import json
import os


class TestPlot(TestCase):

    def setUp(self):
        self.plot = Plot(api='')

    @mock.patch("plot.googlemaps.Client")
    @mock.patch("plot.geocoder")
    @mock.patch("plot.requests.get")
    def test_find_place(self, mock_request, mock_geocoder, mock_gmapsClient):
        mock_request.return_value.text = open("html_for_testing.html", 'r').read()
        mock_geocoder.google.return_value.json = json.load(open("Bembridge Windmill geocoder.json", "r"))
        mock_gmapsClient.return_value.place.return_value = json.load(open("Bembridge Windmill googlemaps.json", "r"))
        self.plot.read_url('test')
        poi = [header.text for header in self.plot.headers]
        output = self.plot.find_place(locations=poi[7], location_supplement="Isle of Wight, UK")
        print(output)
        self.fail()

    @mock.patch("plot.requests.get")
    def test_read_url(self, mock_request):
        mock_request.return_value.text = open("html_for_testing.html", 'r').read()
        self.plot.read_url('test')
        self.assertEqual(self.plot.headers[0].text, '13 Picturesque Places to Visit on the Isle of Wight')

    def test_reset_attribs(self):
        self.plot.headers = ['abc']
        self.plot.links = ['def']
        self.plot.reset_attribs()
        self.assertEqual(self.plot.headers, [])
        self.assertEqual(self.plot.links, [])

    @mock.patch("plot.requests.get")
    def test_filter_list(self, mock_request):
        mock_request.return_value.text = open("html_for_testing.html", 'r').read()
        self.plot.read_url('test')
        output = self.plot.filter_list([header.text for header in self.plot.headers], self.plot.words_filter)
        self.assertEqual(output[0], '13 Picturesque Places Visit Isle Wight')
