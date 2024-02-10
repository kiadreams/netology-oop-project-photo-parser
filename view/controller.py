from view.window import MyWindow
from src.model import Model


class Controller():

    def __init__(self) -> None:
        self.model = None
        self.window = MyWindow()
        self.display = self.window.display_txt
        self.window.set_method_auth_pshbtn(self._connect_model_api)
        self.window.set_method_svd_pshbtn(self._save_photos)
        self.window.set_change_combox(self._set_ph_spin_box)

    def set_progress_bar(self, max_value: int):
        self.window.set_progress_bar(max_value + 0.001)
        self.window.set_text_bar()

    def make_step_progress(self, value: int, text: str):
        self.window.make_step_progressbarr(value)
        self.window.set_text_bar(text)

    def _connect_model_api(self, *args):
        auth_data = [self.window.get_vk_token(),
                     self.window.get_vk_user_id(),
                     self.window.get_yd_token()]
        if all(auth_data):
            model = Model(*auth_data, self)
            self._check_model(model=model)
        else:
            self.display('Заполнены не все поля для авторизации...')

    def _check_model(self, model: Model):
        vk_is_connect, yd_is_connect = model.checking_connect()
        if model.is_working:
            self.model = model
            self.window.clear_display()
            self.display('Подключение к VK и ЯДиску установлено!')
            self._load_model_data()
        elif not vk_is_connect and not yd_is_connect:
            self.display('Введаны НЕПРАВИЛЬНЫЕ ключи доступа к аккаунтам:'
                         'VK и ЯДиск!')
        else:
            text = 'VK аккаунту!' if not vk_is_connect else 'ЯДиску!'
            self.display(f'Не удалось подключиться к {text}')

    def _load_model_data(self):
        album_names = self.model.get_album_names()
        if album_names:
            self._set_albums_box(album_names)
        else:
            self.display('Альбомы не найдены!')

    def _save_photos(self):
        if self.model is not None:
            self.window.clear_display()
            album_name = self.window.get_album_name()
            num_of_photos = self.window.get_num_of_photos()
            if self._data_is_correct(num_of_photos):
                self.model.sv_ph_from_vk_albums(album_name,
                                                int(num_of_photos))
        else:
            self.display('Сервисы не подключены...')

    def _set_albums_box(self, albums: list[str]):
        if 'Фото профиля' in albums:
            self.window.set_albums_box(albums, v_default='Фото профиля')
        else:
            self.window.set_albums_box(albums, v_default=albums[0])
        self._set_ph_spin_box()

    def _set_ph_spin_box(self, *event):
        name = self.window.get_album_name()
        values = list(range(0, self.model.album_names.get(name, 0) + 1))
        self.window.set_vlues_ph(values)

    def _data_is_correct(self, num_of_photos: str) -> bool:
        data_is_correct = False
        if num_of_photos.isdigit() and int(num_of_photos) != 0:
            data_is_correct = True
        elif num_of_photos.isdigit():
            self.display('Количество фотографий для копирования не задано...')
        else:
            self.display('Количество фотографий указано не целым числом...')
        return data_is_correct
