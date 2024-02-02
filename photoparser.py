from src.model import Model
from security.get_token import TOKEN_VK, TOKEN_YD, CLIENT_ID_VK

# client_id = 51843385
# base_url = 'https://oauth.vk.com/authorize'


model = Model(TOKEN_VK, CLIENT_ID_VK, TOKEN_YD)
# print('Все альбомы!')
# model.ld_all_albums()
# print('\nА теперь все фотографии!')
model.vk_ld_ph_from_alb()
model.yd_upld_vk_phs()
# print('\n')
# print(model.ph_names)
# for name in model.photo_names:
#     model.ld_photo_file(name)

# model.yd_ld_disk_info()
# print()
# model.yd_ld_resource_info()

# model.yd_create_dir()
