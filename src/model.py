from os import name
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
        self.yd_folder = 'Копии фото VK'

    def vk_ld_all_albums(self):
        code, resp = self.vk_api.get_photo_albums()
        if code == 200 and resp.get('response', {}):
            for item in resp.get('response', {}).get('items', []):
                album_id = item.get('id')
                self.albums.setdefault(album_id, item)
            pprint(self.albums)
        elif code == 200:
            pprint(resp)
        else:
            print(f'Запрос не удался, код ответа: {code}')
    
    def vk_ld_ph_from_alb(self, album_id=-6):
        code, resp = self.vk_api.get_photos_from_album(album_id)
        if code == 200 and resp.get('response', {}):
            for item in resp.get('response', {}).get('items', []):
                item['sizes'] = max(
                    item.get('sizes', []),
                    key=lambda x: (x.get('height'),x.get('width'))
                    )
                ph_name = self.__get_file_name(item)
                self.photos.setdefault(ph_name, item)
                # pprint(self.photos)
        elif code == 200:
            pprint(resp)
        else:
            print(f'Запрос не удался, код ответа: {code}')

    def vk_sv_photo_to_file(self, photo_name: int):
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
        
    def yd_crt_dir(self, path: str, name: str) -> str:
        resp = self.yd_api.put_new_dir(path=path + name)
        # print(resp)
        return name, resp

    def yd_upld_vk_phs(self, album_id=-6):
        self.vk_ld_ph_from_alb(album_id=album_id)
        if self.photos:
            path = f'{self.yd_crt_dir(path='/', name=self.yd_folder)[0]}/'
            name_album = self.albums.get(album_id, {}).get('title', '')
            path = f'{path}{self.yd_crt_dir(path=path, name=name_album)[0]}/'
            folder_name = dt.now().strftime('%Y-%m-%d_%H%M%S')
            path = f'{path}{self.yd_crt_dir(path=path, name=folder_name)[0]}/'
            for ph_name, ph_data in self.photos.items():
                ph_url = ph_data.get('sizes', {}).get('url')
                path_to_file = f'{path}{ph_name}'
                operation = self.yd_api.post_upload_photo(path_to_file, ph_url)
                print(operation)
                print(f'Файл {ph_name} сохранен...')
            self.photos.clear()

    def yd_status_operation(self):
        pass

    def __get_file_name(self, item: dict) -> str:
        base_url = item.get('sizes', {}).get('url', '').split('?')[0]
        f_exten = base_url.split('.')[-1]
        name = item.get('likes', {}).get('count', 0)
        ph_name = f'{name}.{f_exten}'
        if ph_name in self.photos:
            name += item.get('date')
            ph_name = f'{name}.{f_exten}'
            if ph_name in self.photos:
                name += item.get('id')
                ph_name = f'{name}.{f_exten}'
        return ph_name
