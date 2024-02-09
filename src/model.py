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
        self.contr = controller
        self.is_working = False
        self.albums = {}
        self.album_names = {}
        self.yd_folder = 'Копии фото VK'
        self.result_json_file = []
        self.disp = self.contr.display
        self.progress = [0, 0]

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
        self.progress = [0, 0]
        self.progress[1] = self.__get_num_all_ph(num_photos, album_name)
        self.contr.set_progress_bar()
        if album_name == 'ВСЕ АЛЬБОМЫ':
            for id, album in self.albums.items():
                self.yd_upld_vk_phs(num_photos, album_id=id)
        else:
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
                self.yd_api.post_upload_photo(path_to_file, ph_url)
                self._change_progress()
                self.disp(f'Файл {ph_name} сохранен на ЯДиск...')
                self.__add_record_to_json(ph_name, ph_size)
        else:
            self.disp('Не получилось загрузить фото с альбома!... '
                      'Возможно их в нем нет...')

    def vk_ld_ph_from_alb(self, num_photos: int, album_id=-6) -> dict:
        photos = {}
        code, resp = self.vk_api.get_photos_from_album(album_id)
        if code == 200 and resp.get('response', {}):
            self._change_progress()
            count = 0
            for item in resp.get('response', {}).get('items', []):
                item['sizes'] = max(
                    item.get('sizes', []),
                    key=lambda x: (x.get('height'), x.get('width'))
                )
                ph_name = self._get_file_name(item, photos)
                photos.setdefault(ph_name, item)
                count += 1
                if count == num_photos:
                    break
            self.disp(f'С альбома "{self.albums[album_id].get('title', '')}" '
                      'на VK аккаунте загружены фотографии...')
        elif code == 200:
            self.disp('В ответ пришла ошибка загрузки фото, '
                      'проверте введённые данные')
        else:
            self.disp(f'Запрос не удался, код ответа: {code}')
        return photos

    def vk_sv_photo_to_file(self, photo_name: int, photos: dict):
        photo_url = photos.get(photo_name, {}).get('sizes', {}).get('url')
        resp = requests.get(photo_url)
        if resp.status_code == 200:
            with open(f'{photo_name}.jpg', 'wb') as f:
                f.write(resp.content)
                self.disp('файл записан')

    def yd_ld_disk_info(self):
        resp = self.yd_api.get_disk_info()
        return resp

    def yd_ld_resource_info(self, path='/', limit=20):
        resp = self.yd_api.get_info_recources(path, limit)
        return resp

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
        return vk_status, yd_status
    
    def _change_progress(self):
        self.progress[0] += 1
        self.contr.make_step_progress()

    def _yd_crt_fold_for_ph(self, album_id: int) -> str:
        path = ''
        name_album = self.albums.get(album_id, {}).get('title', '')
        folder_name = dt.now().strftime('%Y-%m-%d_%H%M%S')
        for p in [f'/{self.yd_folder}', f'/{name_album}', f'/{folder_name}']:
            path += p
            resp = self.yd_api.put_new_dir(path)
            self._change_progress()
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
        elif code == 200:
            self.disp('В ответ на запрос - пришла ошбка!!!')
        else:
            self.disp(f'Запрос не удался, код ответа: {code}')

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
        self.disp('Файл json с результатами работы сохранён в корневой '
                  'папке программы!')
        self.result_json_file = []
    
    def __get_num_all_ph(self, num_phs: int, album_name: str) -> int:
        num_all_photos = 0
        if album_name =='ВСЕ АЛЬБОМЫ':
            num_all_photos = sum([min(size, num_phs) + 4
                                  for name, size in self.album_names.items()
                                  if size != 0 and name != 'ВСЕ АЛЬБОМЫ'])
        else:
            album_size = self.album_names.get(album_name, 0)
            num_all_photos += min(album_size, num_phs) + 4
        return num_all_photos
