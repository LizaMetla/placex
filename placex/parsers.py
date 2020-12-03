import json

import requests
from bs4 import BeautifulSoup


def get_all_onliner_rooms(user) -> list:
    params = f"only_owner=true&price%5Bmin%5D={user.price_min or 1}&price%5Bmax%5D={user.price_max or 500}&currency=usd&rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms"
    response = requests.get(
        f"https://ak.api.onliner.by/search/apartments?{params}&bounds%5Blb%5D%5Blat%5D=53.8284204609269&bounds%5Blb%5D%5Blong%5D=27.440757751464847&bounds%5Brt%5D%5Blat%5D=53.96800258730025&bounds%5Brt%5D%5Blong%5D=27.683486938476566")
    print(json.loads(response.content.decode('UTF-8')))
    rooms = json.loads(response.content.decode('UTF-8')).get('apartments')
    rooms_list = []
    for room in rooms:
        address = room.get('location', dict()).get('address')
        rooms_list.append(
            {'link': room.get('url'), 'image': room.get('photo'), 'price': room.get('price').get('amount'),
             'address': address})
    return rooms_list


def get_all_kufar_rooms(user):
    params = {'cat': 1010, 'cur': 'USD',
              'gbx': 'b:27.479209899902344,53.829230976746196,27.699966430664066,53.9764838398327', 'cmp': 0,
              'prc': f'r:{user.price_min},{user.price_max}', 'size': "20", 'sort': 'lst.d',
              'typ': 'let', 'oph': 1}
    response = requests.get("https://re.kufar.by/api/search/ads-search/v1/engine/v1/search/raw", params=params)
    print(str(response.content.decode('UTF-8')))
    rooms = json.loads(response.content.decode('UTF-8'))

    rooms_list = []
    for room in rooms:
        image = room.get("images").pop()
        rooms_list.append({'link': room.get('ad_link'),
                           'image': f'https://content.kufar.by/gallery/{image.get("id")[:2]}/{image.get("id")}.jpg',
                           'price': f"{room.get('price_usd')[:3]}.{room.get('price_usd')[3:]}",
                           'address': room.get('address')})
    return rooms_list


def get_first_or_none(obj_list: list):
    return obj_list[0] if obj_list else None


def get_all_hata_rooms(user) -> list:
    link = f'https://www.hata.by/search/~s_do=rent~s_what=flat~currency=840~cena_from={user.price_min}~cena_to={user.price_max}~ctype=ckod~ckod=5000000000/page/1/'
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    rooms_list = []
    catalog_items = soup.find_all('div', class_='b-catalog-table__item')
    for item in catalog_items:
        img = get_first_or_none(item.find_all(class_='img-fluid'))
        img_link = img.get('data-lazy')

        title = get_first_or_none(item.find_all(class_='title'))
        link = title.a.get('href')
        address = title.a.text
        price = get_first_or_none(item.find_all(class_='price'))
        price_link = price.div.text
        rooms_list.append({'image': img_link,
                           'link': link,
                           'address': address,
                           'price': price_link})
    return rooms_list
