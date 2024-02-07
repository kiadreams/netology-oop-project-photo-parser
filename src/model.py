from os import name
import requests
import json

from datetime import datetime as dt
from pprint import pprint

from src.clients import VKAPIClient, YDAPIClient


class Model():

    def __init__(self, token_vk, client_id_vk, token_yd,
                 controller=None) -> None:
        self.vk_api = VKAPIClient(token_vk, client_id_vk)
        self.yd_api = YDAPIClient(token_yd)
        self.is_working = False
        self.disp = controller.display
        self.progress = controller.progress
        self.albums = {}
        self.album_names = {}
        self.yd_folder = 'Копии фото VK'
        self.result_json_file = []

    def get_album_names(self):
        self._vk_ld_all_albums()
        album_names = {name: album.get('size', 0)
                       for album in self.albums.values()
                       if (name := album.get('title', ''))}
        if album_names:
            album_names.update({'ВСЕ АЛЬБОМЫ': sum(album_names.values())})
        self.album_names = album_names
        return list(self.album_names.keys())

    def sv_ph_from_vk_albums(self, album_name: str, num_photos: int):
        num_all_photo = 0
        if album_name == 'ВСЕ АЛЬБОМЫ':
            num_all_photo = self.__get_num_all_ph()
            for id, album in self.albums.items():
                self.yd_upld_vk_phs(num_photos, album_id=id)
        else:
            num_all_photo = self.__get_num_all_ph()
            id = self.__get_id_album(album_name)
            self.yd_upld_vk_phs(num_photos, album_id=id)
        if self.result_json_file:
            self.__save_result_json_file()
    
    def yd_upld_vk_phs(self, num_photos: int, album_id=-6):
        photos = self.vk_ld_ph_from_alb(num_photos, album_id=album_id)
        if photos:
            path = self._yd_crt_fold_for_ph(album_id)
            for ph_name, ph_data in photos.items():
                ph_url = ph_data.get('sizes', {}).get('url')
                ph_size = ph_data.get('sizes', {}).get('type')
                path_to_file = f'{path}{ph_name}'
                operation = self.yd_api.post_upload_photo(path_to_file, ph_url)
                print(operation)
                print(f'Файл {ph_name} сохранен...')
                self.__add_record_to_json(ph_name, ph_size)
        else:
            self.disp('Не получилось загрузить фото с альбома!... '
                      'Возможно их в нем нет...')

    def vk_ld_ph_from_alb(self, num_photos: int, album_id=-6) -> dict:
        photos = {}
        code, resp = self.vk_api.get_photos_from_album(album_id)
        if code == 200 and resp.get('response', {}):
            count = 0
            for item in resp.get('response', {}).get('items', []):
                item['sizes'] = max(
                    item.get('sizes', []),
                    key=lambda x: (x.get('height'), x.get('width'))
                )
                ph_name = self._get_file_name(item, photos)
                photos.setdefault(ph_name, item)
                pprint(photos)
                count += 1
                if count == num_photos:
                    break
        elif code == 200:
            pprint(resp)
        else:
            print(f'Запрос не удался, код ответа: {code}')
        return photos

    def vk_sv_photo_to_file(self, photo_name: int, photos: dict):
        photo_url = photos.get(photo_name, {}).get('sizes', {}).get('url')
        resp = requests.get(photo_url)
        if resp.status_code == 200:
            with open(f'{photo_name}.jpg', 'wb') as f:
                f.write(resp.content)
                print('файл записан')

    def yd_ld_disk_info(self):
        pprint(self.yd_api.get_disk_info())

    def yd_ld_resource_info(self, path='/', limit=20):
        pprint(self.yd_api.get_info_recources(path, limit))

    def yd_crt_dir(self, path: str) -> str:
        resp = self.yd_api.put_new_dir(path)
        return resp

    def checking_connect(self):
        vk_is_connect = self.vk_api.get_albums_count()
        yd_is_connect = self.yd_api.get_disk_info()
        vk_status = vk_is_connect[1].get('response', {})
        yd_status = yd_is_connect[0] == 200
        if vk_status and yd_status:
            self.is_working = True
        print(vk_is_connect, yd_is_connect)
        return vk_status, yd_status

    def _yd_crt_fold_for_ph(self, album_id: int) -> str:
        path = ''
        name_album = self.albums.get(album_id, {}).get('title', '')
        folder_name = dt.now().strftime('%Y-%m-%d_%H%M%S')
        for p in [f'/{self.yd_folder}', f'/{name_album}', f'/{folder_name}']:
            path += p
            resp = self.yd_api.put_new_dir(path)
            print(path, resp[0])
        return path + '/'

    def _yd_status_operation(self):
        pass

    def _get_file_name(self, item: dict, photos: dict) -> str:
        base_url = item.get('sizes', {}).get('url', '').split('?')[0]
        f_exten = base_url.split('.')[-1]
        name = item.get('likes', {}).get('count', 0)
        ph_name = f'{name}.{f_exten}'
        if ph_name in photos:
            name += item.get('date')
            ph_name = f'{name}.{f_exten}'
            if ph_name in photos:
                name += item.get('id')
                ph_name = f'{name}.{f_exten}'
        return ph_name

    def _vk_ld_all_albums(self):
        code, resp = self.vk_api.get_photo_albums()
        if code == 200 and resp.get('response', {}):
            for item in resp.get('response', {}).get('items', []):
                album_id = item.get('id')
                self.albums.setdefault(album_id, item)
            # self.disp(self.albums)
        elif code == 200:
            pprint(resp)
        else:
            print(f'Запрос не удался, код ответа: {code}')

    def __get_id_album(self, album_name: str) -> int:
        result_id = -6
        for id, album in self.albums.items():
            if album.get('title') == album_name:
                result_id = id
                break
        return result_id

    def __add_record_to_json(self, ph_name: str, ph_size: str):
        record = {'file_name': ph_name, 'size': ph_size}
        self.result_json_file.append(record)

    def __save_result_json_file(self):
        json_file_name = f'result_{dt.now().strftime('%H%M%S')}.json'
        with open(json_file_name, 'w') as f_out:
            json.dump(self.result_json_file, f_out, ensure_ascii=False,
                      indent=2)
        self.result_json_file = []
    
    def __get_num_all_ph(self, num_of_photos: int,
                         is_all_albums=False,
                         album_name=None) -> int:
        num_all_photos = 0
        if is_all_albums:
            for sizes in self.album_names.values():
                num_all_photos += min(sizes, num_of_photos)
        else:
            num_all_photos = self.album_names.get(album_name, 0)
        return num_all_photos
            
            
