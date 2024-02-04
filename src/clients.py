import requests

from urllib.parse import urlencode


# https://<адрес-сервера>/method/<имя-API-метода>?<параметры>
# api.vk.com
# api.vk.ru
# photos.get
class VKAPIClient():
    BASE_VK_URL = 'https://api.vk.com/method/'
    
    def __init__(self, access_token_vk: str,
                 user_id: str,
                 version_vk_api='5.199') -> None:
        self.token = access_token_vk
        self.user_id = user_id
        self.version_vk_api = version_vk_api
        self.params = {'access_token': self.token, 'v': self.version_vk_api}
    
    def get_albums_count(self):
        params = {'user_id': self.user_id,
                   **self.params}
        resp = requests.get(f'{self.BASE_VK_URL}photos.getAlbumsCount', params)
        return resp.status_code, resp.json()

    
    def get_all_photo(self, extended=True, photo_sizes=False) -> tuple:
        params  = {'extended': extended,
                   'photo_sizes': photo_sizes,
                   **self.params}
        resp = requests.get(f'{self.BASE_VK_URL}photos.getAll', params)
        return resp.status_code, resp.json()
        
    def get_photos_from_album(self, album_id: int,
                              photo_sizes=True,
                              extended=True) -> tuple:
        params = {'owner_id': self.user_id,
                  'album_id': album_id,
                  'photo_sizes': photo_sizes,
                  'extended': extended,
                  **self.params}
        resp = requests.get(f'{self.BASE_VK_URL}photos.get', params)
        return resp.status_code, resp.json()
    
    def get_photo_albums(self, need_system=True, need_covers=True) -> tuple:
        params = {'owner_id': self.user_id,
                  'need_system': need_system,
                  'need_covers': need_covers,
                  **self.params}
        resp = requests.get(f'{self.BASE_VK_URL}photos.getAlbums', params)
        return resp.status_code, resp.json()


class YDAPIClient():
    BASE_YD_URL = 'https://cloud-api.yandex.net/v1/disk/'
    
    def __init__(self, token_yd) -> None:
        self.headers = {'Accept': 'application/json',
                        'Authorization': token_yd}
    
    def get_disk_info(self) -> tuple:
        resp = requests.get(self.BASE_YD_URL, headers=self.headers)
        return resp.status_code, resp.json
    
    def get_info_recources(self, path, limit) -> dict:
        url = f'{self.BASE_YD_URL}resources'
        params = {'path': path, 'limit': limit}
        return requests.get(url, params=params, headers=self.headers).json()
    
    def put_new_dir(self, path='/') -> dict:
        url = f'{self.BASE_YD_URL}resources'
        params = {'path': path}
        resp = requests.put(url, params=params, headers=self.headers)
        return resp.status_code, resp.json()
    
    def post_upload_photo(self, path: str, file_url: str) -> dict:
        url = f'{self.BASE_YD_URL}resources/upload'
        params = {'path': path, 'url': file_url}
        resp = requests.post(url, params=params, headers=self.headers)
        return resp.status_code, resp.json()


if __name__ == '__main__':
    
    client_id = 51843385
    base_url = 'https://oauth.vk.com/authorize'
    
    
    def get_request_string(vk_url: str, app_id: int) -> str:
        vk_params = {
            'client_id': app_id,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': 6,
            'response_type': 'token'
        }
        return f'{vk_url}?{urlencode(vk_params)}'


    print(get_request_string(base_url, client_id))
