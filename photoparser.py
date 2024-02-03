from urllib.parse import urlencode
import requests
from src.model import Model
from security.get_token import TOKEN_VK, TOKEN_YD, CLIENT_ID_VK

# client_id = 51843385
# base_url = 'https://oauth.vk.com/authorize'


model = Model(TOKEN_VK, CLIENT_ID_VK, TOKEN_YD)
# print('Все альбомы!')
# model.ld_all_albums()
# print('\nА теперь все фотографии!')
model.vk_ld_ph_from_alb()
print()
model.yd_upld_vk_phs()
# print('\n')
# print(model.ph_names)
# for name in model.photo_names:
#     model.ld_photo_file(name)

# model.yd_ld_disk_info()
# print()
# model.yd_ld_resource_info()

# model.yd_create_dir()



# Файл get_token.py
# client_id = 51843385
# base_url = 'https://oauth.vk.com/authorize'


# TOKEN_VK = ('vk1.a.exKgeZkJPvvZkMvXO4JolnSfOx_72Tq9Tp-EaQmmzdj3ASvLa7XdPMIme0ZkuB5jmzkYfbY5NxuwDuz9rmPW6cjAIbAhxLwrxo6HfNZ0w0e1IYJU-As6IOdismbQ4f1U_ZO85ZPxvpPGYZRjsuCrjtSW8DFgrWy28WC1Vv7mPygTB2XCUKUZmtKXoIbn14zC')
# CLIENT_ID_VK = 187352442

# TOKEN_YD = 'y0_AgAAAABzy31PAADLWwAAAAD5btLjAADAP5-awe9BcofulWuuwzLjOn6dHA'

# def get_vk_token():
#     vk_params = {
#         'client_id': 51843385,
#         'redirect_uri': 'https://oauth.vk.com/blank.html',
#         'display': 'page',
#         'scope': 6,
#         'response_type': 'token'
#     }
#     res = requests.get(base_url,
#                        params=vk_params)
#     print(res.status_code)
#     print(res.text)


# def get_request_string(vk_url: str, app_id: int) -> str:
#     vk_params = {
#         'client_id': app_id,
#         'redirect_uri': 'https://oauth.vk.com/blank.html',
#         'display': 'page',
#         'scope': 6,
#         'response_type': 'token'
#     }
#     return f'{vk_url}?{urlencode(vk_params)}'


# print(get_request_string(base_url, client_id))
