import requests


# https://<адрес-сервера>/method/<имя-API-метода>?<параметры>
# api.vk.com
# api.vk.ru
# photos.get
class VKAPIClient():
    BASE_VK_URL = 'https://api.vk.com/method/'
    VERSION_VK_API = '5.199'
    
    def __init__(self, token_vk: str, user_id: str) -> None:
        self.token = token_vk
        self.user_id = str(user_id)
        
    def get_all_photo(self, extended=True, photo_sizes=False) -> tuple:
        method = 'photos.getAll'
        some_params  = {
            'extended': extended,
            'photo_sizes': photo_sizes,
            }
        return self.__execute_request(method, some_params)
        
    def get_photos_from_album(self, album_id, photo_sizes=True,
                              extended=True) -> tuple:
        method = 'photos.get'
        some_params = {
            'owner_id': self.user_id,
            'album_id': album_id,
            'photo_sizes': photo_sizes,
            'extended': extended,
        }
        return self.__execute_request(method, some_params)
    
    def get_photo_albums(self) -> tuple:
        method = 'photos.getAlbums'
        some_params = {
            'owner_id': self.user_id,
        }
        return self.__execute_request(method, some_params)
        
    def __execute_request(self, method: str, some_params: dict) -> tuple:
        some_params.update({'access_token': self.token,
                            'v': self.VERSION_VK_API})
        resp = requests.get(f'{self.BASE_VK_URL}{method}', some_params)
        return resp.status_code, resp.json()


class YDAPIClient():
    BASE_YD_URL = 'https://cloud-api.yandex.net/v1/disk/'
    
    def __init__(self, token_yd) -> None:
        self.headers = {'Accept': 'application/json',
                        'Authorization': token_yd}
    
    def get_disk_info(self) -> dict:
        return requests.get(self.BASE_YD_URL, headers=self.headers).json()
    
    def get_info_recources(self, path, limit) -> dict:
        url = f'{self.BASE_YD_URL}resources'
        params = {'path': path, 'limit': limit}
        return requests.get(url, params=params, headers=self.headers).json()
    
    def put_new_dir(self, path='/') -> dict:
        url = f'{self.BASE_YD_URL}resources'
        params = {'path': path}
        resp = requests.put(url, params=params, headers=self.headers)
        return resp.json()
    
    def post_upload_photo(self, path: str, file_url: str) -> dict:
        url = f'{self.BASE_YD_URL}resources/upload'
        params = {'path': path, 'url': file_url}
        resp = requests.post(url, params=params, headers=self.headers)
        return resp.status_code, resp.json()
