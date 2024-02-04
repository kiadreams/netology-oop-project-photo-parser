from view.window import MyWindow
from src.model import Model

class Controller():

    def __init__(self) -> None:
        self.window = MyWindow()
        self.model = None
        self.model_is_working = False
        self.window.btn_svd_photo.config(command=self.crt_model_api)
        # self.window.entr_vk_id.bind('<Activate>', self.crt_model_api)
        # self.window.entr_vk_token.bind('<KeyPress>', self.crt_model_api)
        # self.window.entr_yd_token.bind('<KeyPress>', self.crt_model_api)
        # self.window.mainloop()
        # self.vk_user_id = ''
        # self.vk_token = ''
        # self.yd_token = ''
        # self.window.entr_vk_id.var

    def crt_model_api(self, event=None):
        print('сработал', event)
        if (self.window.vk_user_id.get()
                and self.window.vk_token.get()
                and self.window.yd_token.get()):
            if not self.model_is_working:
                self.model = Model(self.window.vk_token,
                                self.window.vk_user_id,
                                self.window.yd_token)
            print('Модель подключена!')
            return None
        self.window.text_editor.print('Не все поля заполнены')
