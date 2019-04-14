from unittest import TestCase
from unittest import mock
from plot import Plot

class TestPlot(TestCase):

    def setUp(self):
        self.plot = Plot(api = '')

    #@mock.patch("plot.requests.get")
    def test_find_place(self):
        self.fail()

    @mock.patch("plot.requests.get")
    def test_read_url(self, mock_request):
        mock_request.return_value.text = open("html_for_testing.html",'r').read()
        a = self.plot.read_url('test')
        self.assertEqual(a[0].text,'13 Picturesque Places to Visit on the Isle of Wight')

    def test_read_file(self):
        self.fail()
