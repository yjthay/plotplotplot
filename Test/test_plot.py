from unittest import TestCase
from unittest import mock
from plot import Plot
import json
import os


class TestPlot(TestCase):

    @mock.patch("plot.googlemaps.Client")
    def setUp(self, mock_gmaps):
        with open("Bembridge Windmill googlemaps.json", "r") as f:
            mock_gmaps.return_value.place.return_value = json.load(f)
        self.plot = Plot(api='')

    @mock.patch("plot.webbrowser")
    @mock.patch("plot.geocoder")
    @mock.patch("plot.requests.get")
    def test_find_place(self, mock_request,mock_geocoder,mock_webbrower):
        with open("html_for_testing.html", 'r') as f:
            mock_request.return_value.text = f.read()
        with open("Bembridge Windmill geocoder.json", "r") as f:
            mock_geocoder.google.return_value.json = json.load(f)
        self.plot.read_url('test')
        mock_webbrower.open.return_value = "Open weblink"
        poi = [header.text for header in self.plot.headers]
        output = self.plot.find_place(locations=poi[7], location_supplement="Isle of Wight, UK")
        with open('Bembridge Windmill.json','r') as f:
            expected = json.load(f)
        self.assertEqual(1, mock_webbrower.open.call_count)
        mock_webbrower.open.assert_called_with(expected["Bembridge Windmill"]['url'])
        self.assertEqual(expected, output)

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
