import json
import re
import time

import requests
from bs4 import BeautifulSoup

from rent.models import Advert


def get_first_or_none(obj_list: list):
    return obj_list[0] if obj_list else None
def get_all_onliner_rooms() -> list:
    params = f"price%5Bmin%5D=1&price%5Bmax%5D=1000&currency=usd&rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms"
    response = requests.get(
        f"https://ak.api.onliner.by/search/apartments?{params}&bounds%5Blb%5D%5Blat%5D=53.8284204609269&bounds%5Blb%5D%5Blong%5D=27.440757751464847&bounds%5Brt%5D%5Blat%5D=53.96800258730025&bounds%5Brt%5D%5Blong%5D=27.683486938476566")
    print(json.loads(response.content.decode('UTF-8')))
    rooms = json.loads(response.content.decode('UTF-8')).get('apartments')
    rooms_list = []
    for room in rooms:
        if Advert.objects.filter(link=room.get('url')).exists():
            continue
        address = room.get('location', dict()).get('address')
        room_page = requests.get(room.get('url')).text
        time.sleep(3)
        images_urls = []
        description = ''
        count_room = room.get('rent_type')
        count_room = {'1_room': 1,
         '2_rooms': 2,
         '3_rooms': 3,
         '4_rooms': 4}.get(count_room, 1)
        try:
            images_objs = BeautifulSoup(room_page, "html.parser").find_all('div', class_='apartment-cover__thumbnail')
            description = get_first_or_none(BeautifulSoup(room_page, "html.parser").find_all('div', class_='apartment-info__sub-line apartment-info__sub-line_extended-bottom')).text
            if description:
                description = ' '.join(description.split())
            for images_obj in images_objs:
                image_url = re.search(r"(?:\(['\"]?)(.*?)(?:['\"]?\))", images_obj.attrs.get('style')).group(1)
                if image_url and image_url!=room.get('photo'):
                    images_urls.append(image_url)
        except:
            pass
        rooms_list.append(
            {'link': room.get('url'), 'image': room.get('photo'), 'price': float(room.get('price').get('amount')),
             'address': address, 'images': images_urls, 'description': description, 'is_agent': not room.get('contact').get('owner'), 'count_room':count_room})
    return rooms_list


def get_all_kufar_rooms():
    params = {'cat': 1010, 'cur': 'USD',
              'gbx': 'b:27.479209899902344,53.829230976746196,27.699966430664066,53.9764838398327', 'cmp': 0,
              'prc': f'r:1,1000', 'size': "20", 'sort': 'lst.d',
              'typ': 'let', 'oph': 1}
    response = requests.get("https://re.kufar.by/api/search/ads-search/v1/engine/v1/search/raw", params=params)
    print(str(response.content.decode('UTF-8')))
    rooms = json.loads(response.content.decode('UTF-8'))

    rooms_list = []
    for room in rooms:
        image = room.get("images").pop()
        prices = re.findall(r'\d+', room.get('price_usd')[:3])
        if len(prices) >= 1:
            price = float(prices[0])
        else:
            price = 10.0
        rooms_list.append({'link': room.get('ad_link'),
                           'image': f'https://content.kufar.by/gallery/{image.get("id")[:2]}/{image.get("id")}.jpg',
                           'price': price,
                           'address': room.get('address')})
    return rooms_list





def get_all_hata_rooms() -> list:
    link = f'https://www.hata.by/search/~s_do=rent~s_what=flat~currency=840~cena_from=1~cena_to=1000~ctype=ckod~ckod=5000000000/page/1/'
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    rooms_list = []
    catalog_items = soup.find_all('div', class_='b-catalog-table__item')
    for item in catalog_items:
        img = get_first_or_none(item.find_all(class_='img-fluid'))
        description = ' '.join(item.find_all(class_='description')[0].text.split())
        img_link = img.get('data-lazy')
        images = []
        for i, image_obj in enumerate(item.find_all(class_='img-fluid')):
            if i == 0:
                continue
            images.append(image_obj.get('data-lazy'))
        title = get_first_or_none(item.find_all(class_='title'))
        link = title.a.get('href')
        address = title.a.text
        price = get_first_or_none(item.find_all(class_='price'))
        price_link = price.div.text
        prices = re.findall(r'\d+', price_link)
        if len(prices) >= 1:
            price = float(prices[0])
        else:
            price = 10.0
        rooms_list.append({'image': img_link,
                           'link': link,
                           'address': " ".join(address.split()),
                           'price': price,
                           'images': images,
                           'is_agent': False,
                           'description': description})

    return rooms_list
