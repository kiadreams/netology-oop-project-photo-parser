from tkinter import END
from view.window import MyWindow
from src.model import Model

class Controller():

    def __init__(self) -> None:
        self.window = MyWindow()
        self.model = None
        self.model_is_working = False
        self.window.btn_svd_photo.config(command=self.crt_model_api)
        self.window.vk_token.trace_add('write', self.crt_model_api)
        self.window.vk_user_id.trace_add('write', self.crt_model_api)
        self.window.yd_token.trace_add('write', self.crt_model_api)

    def crt_model_api(self, *args):
        print('метод сработал', args)
        vk_user_id = self.window.vk_user_id.get()
        vk_token = self.window.vk_token.get()
        yd_token = self.window.yd_token.get()
        if all([vk_user_id, vk_token, yd_token, not self.model_is_working]):
            self.model = Model(vk_token, vk_user_id, yd_token)
            self.model_is_working = self.model.checking_connect()
            if self.model_is_working:
                self.window.text_editor.insert(END, 'Модель подключена!\n')
            return None
        self.window.text_editor.insert(END, 'Не все поля заполнены\n')

