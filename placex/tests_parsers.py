import requests
from django.test import TestCase
from bs4 import BeautifulSoup

from placex.parsers import get_all_hata_rooms, get_all_onliner_rooms


class UserMock():
    def __init__(self):
        self.price_min = 400
        self.price_max = 510

class KufarTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = UserMock()

    def test_get_response(self):
        params = {'cur': 'USD',
                  'gbx': 'b:27.457481825832204,53.829230976746196,27.680984938625176,54.002466983521714',
                  'prc': f'r:{self.user.price_min},{self.user.price_max}', 'oph': 1}
        response = requests.get("https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/bez-posrednikov/", params=params)
        soup = BeautifulSoup(response.text, "html.parser")
class OnlinerTest(TestCase):
    def test_onliner(self):
        rooms = get_all_hata_rooms()
        self.assertTrue(len(rooms)> 0)