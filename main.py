import requests
import config
from pprint import pprint


vk_token = config.vk_token
url = 'https://api.vk.com/method/photos.get'
params = {
    'owner_id': '11606581',
    'album_id': 'profile',
    'extended': '1',
    'photo_sizes': '1',
    'rev': '1',
    'access_token': vk_token,
    'v': '5.131'
}
response = requests.get(url, params=params).json()
#pprint(response)

def get_link(response = response, i=int):
    for j in response['response']['items'][i]['sizes']:
        if j['type'] == 'z':
            return j['url']
def get_photo():
    for i in range(5):
        file_name = response['response']['items'][i]['likes']['count']
        link = get_link(response, i)
        f = open(f'{file_name}.jpg', 'wb')
        ufr = requests.get(link)
        f.write(ufr.content)
        f.close()
# get_photo()
