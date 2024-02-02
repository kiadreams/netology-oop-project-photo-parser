import requests
from datetime import datetime as dt

from pprint import pprint

from src.clients import VKAPIClient, YDAPIClient


class Model():

    def __init__(self, token_vk, client_id_vk, token_yd) -> None:
        self.vk_api = VKAPIClient(token_vk, client_id_vk)
        self.yd_api = YDAPIClient(token_yd)
        self.albums = {}
        self.photos = {}
        # self.ph_names = []
        self.yd_fld_name = None

    def vk_ld_all_albums(self):
        photo_albums = self.vk_api.get_photo_albums()
        for item in photo_albums.get('response', {}).get('items', []):
            album_id = item.get('id')
            self.albums.setdefault(album_id, item)
        # print('Получили список альбомов, ждём 3 секунды')
        # print('... и выводим результат')
        # print(type(photo_albums))
        # time.sleep(3)
        pprint(self.albums)
    
    def vk_ld_ph_from_alb(self, album_id='profile'):
        code, resp = self.vk_api.get_photos_from_album(album_id)
        if code == 200 and resp.get('response', {}):
            for item in resp.get('response', {}).get('items', []):
                ph_name = item.get('likes').get('count')
                if ph_name in self.photos:
                    ph_name += item.get('date')
                    if ph_name in self.photos:
                        ph_name += item.get('id')
                item['sizes'] = max(
                    item.get('sizes', []),
                    key=lambda x: (x.get('height'),x.get('width'))
                    )
                self.photos.setdefault(ph_name, item)
                pprint(self.photos)
        elif code == 200:
            pprint(resp)
        else:
            print(f'Запрос не удался, код ответа: {code}')

    def vk_ld_photo_file(self, photo_name: int):
        photo_url = self.photos.get(photo_name, {}).get('sizes', {}).get('url')
        resp = requests.get(photo_url)
        if resp.status_code == 200:
            with open(f'{photo_name}.jpg', 'wb') as f:
                f.write(resp.content)
                print('файл записан')
    
    def yd_ld_disk_info(self):
        pprint(self.yd_api.get_disk_info())
    
    def yd_ld_resource_info(self, path='/', limit=20):
        pprint(self.yd_api.get_info_recources(path, limit))
        
    def yd_create_dir(self, path='/') -> str:
        folder_name = dt.now().strftime('%Y-%m-%d_%H%M%S')
        resp = self.yd_api.put_new_dir(path=path + folder_name)
        print(resp)
        return folder_name

    def yd_upld_vk_phs(self):
        if self.yd_fld_name is None:
            self.yd_fld_name = self.yd_create_dir()
        else:
            for ph_name, ph_data in self.photos.items():
                ph_url = ph_data.get('sizes', {}).get('url')
                self.yd_api.post_upload_photo(self.yd_fld_name, ph_url)
                print(f'Файл {ph_name} сохранен...')
