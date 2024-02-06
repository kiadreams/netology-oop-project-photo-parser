import tkinter as tk

from tkinter import END, ttk as tkttk
from tkinter.scrolledtext import ScrolledText

from security.get_token import TOKEN_VK, TOKEN_YD, CLIENT_ID_VK

class MyWindow(tk.Tk):

    def __init__(self, screenName: str | None = None,
                 baseName: str | None = None,
                 className: str = "Tk",
                 useTk: bool = True,
                 sync: bool = False,
                 use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry('800x600')
        self.title('Приложение резервного копирования фото с VK')
        self._distination = tk.StringVar(value="яндекс")
        self.vk_user_id = tk.StringVar(value=CLIENT_ID_VK) # ''
        self.vk_token = tk.StringVar(value=TOKEN_VK)   # ''
        self.yd_token = tk.StringVar(value=TOKEN_YD)   # ''
        self._value_album = tk.StringVar(value='')
        self._crt_btn_svd_photo()
        self._crt_btn_auth()
        self._crt_alb_combox()
        self._crt_progressbar()
        self._set_grid()
        self._crt_label_album()
        self._crt_label_photo()
        self._crt_spinbox_nums_ph()
        self._crt_label_vk_user_id()
        self._crt_entr_vk_id()
        self._crt_label_vk_token()
        self._crt_entr_vk_token()
        self._crt_label_yd_token()
        self._crt_entr_yd_token()
        self._crt_label_distinat()
        self._crt_radbtn_distinat_1()
        self._crt_text_editor()

    def display_txt(self, text: str):
        self._text_editor.insert(END, f'{text}\n')

    def get_vk_user_id(self):
        return self.vk_user_id.get()

    def get_vk_token(self):
        return self.vk_token.get()

    def get_yd_token(self):
        return self.yd_token.get()

    def set_albums_box(self, album_names: list[str], v_default=''):
        self.__alb_box.configure(values=album_names)
        self.__alb_box.set(v_default)
        print(album_names)

    def set_vlues_ph(self, nums: list[str]):
        self.__spinbox_photo.configure(values=nums)
        self.__spinbox_photo.set(value=5 if 5 in nums else max(nums))

    def set_method_auth_pshbtn(self, __function):
        self.__btn_auth.config(command=__function)

    def set_method_svd_pshbtn(self, __function):
        self.__btn_svd_photo.config(command=__function)

    def get_album_name(self):
        return self.__alb_box.get()
    
    def get_num_of_photos(self):
        return self.__spinbox_photo.get()

    def set_change_combox(self, __finction):
        self.__alb_box.bind("<<ComboboxSelected>>", __finction)

    def _set_grid(self):
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)
        self.columnconfigure(index=4, weight=1)
        self.columnconfigure(index=5, weight=1)
        self.columnconfigure(index=6, weight=4)
        self.columnconfigure(index=7, weight=4)
        self.columnconfigure(index=8, weight=4)
        self.columnconfigure(index=9, weight=4)
        self.columnconfigure(index=10, weight=4)
        self.columnconfigure(index=11, weight=4)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.rowconfigure(index=4, weight=1)
        self.rowconfigure(index=5, weight=4)
        self.rowconfigure(index=6, weight=4)
        self.rowconfigure(index=7, weight=4)
        self.rowconfigure(index=8, weight=4)
        self.rowconfigure(index=9, weight=1)
        self.rowconfigure(index=10, weight=4)
        self.rowconfigure(index=11, weight=2)

    def _crt_btn_auth(self):
        self.__btn_auth = tkttk.Button(self, text='Подключиться к СЕРВИСАМ')
        self.__btn_auth.grid(column=10, row=4, sticky='nsew',
                             padx=10, pady=5, columnspan=2)

    def _crt_btn_svd_photo(self):
        self.__btn_svd_photo = tkttk.Button(self, text='Сохранить фото')
        self.__btn_svd_photo.grid(column=11, row=9, sticky='nsew', padx=10)

    def _crt_alb_combox(self):
        self.__alb_box = tkttk.Combobox(self)
        self.__alb_box.grid(column=1, row=7, columnspan=2, sticky='nwe',
                            padx=10)

    def _crt_progressbar(self):
        self.progressbarr = tkttk.Progressbar(self)
        self.progressbarr.grid(column=1, row=9, sticky='ew',
                               columnspan=10,
                               padx=30, pady=1)

    def _crt_label_album(self):
        self.__label_album = tkttk.Label(self, text='ВЫБЕРИТЕ АЛЬБОМ')
        self.__label_album.grid(column=1, row=6, columnspan=2, sticky='swe',
                                padx=10)

    def _crt_label_photo(self):
        self.__label_photo = tkttk.Label(
            self,
            text='кол-во фото\n(" " копировать все)'
        )
        self.__label_photo.grid(column=3, row=6, sticky='swe', padx=10)

    def _crt_spinbox_nums_ph(self):
        self.__spinbox_photo = tkttk.Spinbox(self, wrap=True, justify='center')
        self.__spinbox_photo.grid(column=3, row=7, sticky='wn', padx=10)

    def _crt_label_vk_user_id(self):
        self.__label_vk_user_id = tkttk.Label(
            self,
            text='Введите id пользователя VK'
        )
        self.__label_vk_user_id.grid(column=1, row=4, columnspan=1,
                                     sticky='w', pady=5, padx=10)

    def _crt_entr_vk_id(self):
        self.entr_vk_id = tkttk.Entry(self, textvariable=self.vk_user_id)
        self.entr_vk_id.grid(column=2, row=4, columnspan=2, sticky='we',
                             padx=10, pady=5)

    def _crt_label_vk_token(self):
        self.__label_vk_token = tkttk.Label(
            self,
            text='Введите ключ доступа к аккаунту VK'
        )
        self.__label_vk_token.grid(column=1, row=1, columnspan=11,
                                   sticky='ws', pady=5, padx=10)

    def _crt_entr_vk_token(self):
        self.entr_vk_token = tk.Entry(self, textvariable=self.vk_token)
        self.entr_vk_token.grid(column=1, row=2, columnspan=11, sticky='new',
                                padx=10, pady=5)

    def _crt_label_yd_token(self):
        self.__label_yd_token = tkttk.Label(
            self,
            text='Введите ключ доступа к яндекс ДИСКУ'
        )
        self.__label_yd_token.grid(column=1, row=3, columnspan=2, sticky='wn',
                                   pady=10, padx=10)

    def _crt_entr_yd_token(self):
        self.entr_yd_token = tkttk.Entry(self, textvariable=self.yd_token)
        self.entr_yd_token.grid(column=3, row=3, columnspan=9, sticky='ewn',
                                padx=10, pady=10)

    def _crt_label_distinat(self):
        self.__label_distance = tkttk.Label(self, text='Куда копировать:')
        self.__label_distance.grid(column=7, row=6, columnspan=2,
                                   sticky='wse')

    def _crt_radbtn_distinat_1(self):
        self.radbtn_distinat_1 = tkttk.Radiobutton(self, text='Яндекс ДИСК',
                                                   value='яндекс',
                                                   variable=self._distination)
        self.radbtn_distinat_1.grid(column=7, row=7, columnspan=2,
                                    sticky='nwe', padx=10, pady=2)

    def _crt_text_editor(self):
        self._text_editor = ScrolledText(self, height=10)
        self._text_editor.grid(column=1, row=10, columnspan=11,
                               rowspan=2, sticky='nsew', padx=10, pady=5)


if __name__ == '__main__':
    window = MyWindow()

    # window = tk.Tk()
    # window.title("Добро пожаловать в приложение PythonRu")
    # window.geometry('400x250')
    # lbl = tk.Label(window, text="Привет", font=("Arial Bold", 50))
    # lbl.grid(column=0, row=0)
    # btn = tk.Button(window, text="Не нажимать!")
    # btn.grid(column=1, row=0)

    window.mainloop()
