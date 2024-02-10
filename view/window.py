import tkinter as tk

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


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
        self.__distination = tk.StringVar(value="яндекс")
        self.__vk_user_id = tk.StringVar(value='')
        self.__vk_token = tk.StringVar(value='')
        self.__yd_token = tk.StringVar(value='')
        self.__value_bar = tk.IntVar(value=0)
        # self.__text_bar = tk.StringVar(value='Первоначальный элемент')
        # Application interface
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
        self.__label_vk_token = ttk.Label(
            self,
            text='Введите ключ доступа к аккаунту VK'
        )
        self.__label_vk_token.grid(
            column=1, row=1, columnspan=11, sticky='ws', pady=5, padx=10
        )
        self.__entr_vk_token = tk.Entry(self, textvariable=self.__vk_token)
        self.__entr_vk_token.grid(
            column=1, row=2, columnspan=11, sticky='new', padx=10, pady=5
        )
        self.__label_yd_token = ttk.Label(
            self,
            text='Введите ключ доступа к яндекс ДИСКУ'
        )
        self.__label_yd_token.grid(
            column=1, row=3, columnspan=2, sticky='wn', pady=10, padx=10
        )
        self.__entr_yd_token = ttk.Entry(self, textvariable=self.__yd_token)
        self.__entr_yd_token.grid(
            column=3, row=3, columnspan=9, sticky='ewn', padx=10, pady=10
        )
        self.__label_vk_user_id = ttk.Label(
            self,
            text='Введите id пользователя VK'
        )
        self.__label_vk_user_id.grid(
            column=1, row=4, columnspan=1, sticky='w', pady=5, padx=10
        )
        self.__entr_vk_id = ttk.Entry(self, textvariable=self.__vk_user_id)
        self.__entr_vk_id.grid(
            column=2, row=4, columnspan=2, sticky='we', padx=10, pady=5
        )
        self.__btn_auth = ttk.Button(self, text='Подключиться к СЕРВИСАМ')
        self.__btn_auth.grid(
            column=10, row=4, sticky='nsew', padx=10, pady=5, columnspan=2
        )
        self.__label_album = ttk.Label(self, text='ВЫБЕРИТЕ АЛЬБОМ')
        self.__label_album.grid(
            column=1, row=6, columnspan=2, sticky='swe', padx=10
        )
        self.__alb_box = ttk.Combobox(self, state='readonly')
        self.__alb_box.grid(
            column=1, row=7, columnspan=2, sticky='nwe', padx=10
        )
        self.__label_photo = ttk.Label(
            self, text='кол-во фото\n(" " копировать все)'
        )
        self.__label_photo.grid(column=3, row=6, sticky='swe', padx=10)
        self.__spinbox_photo = ttk.Spinbox(self, wrap=True, justify='center')
        self.__spinbox_photo.grid(column=3, row=7, sticky='wn', padx=10)
        self.__label_distance = ttk.Label(self, text='Куда копировать:')
        self.__label_distance.grid(
            column=7, row=6, columnspan=2, sticky='wse'
        )
        self.__radbtn_distinat_1 = ttk.Radiobutton(
            self, text='Яндекс ДИСК',
            value='яндекс',
            variable=self.__distination
        )
        self.__radbtn_distinat_1.grid(
            column=7, row=7, columnspan=2, sticky='nwe', padx=10, pady=2
        )
        self.style_prbr = ttk.Style()
        self.style_prbr.layout(
            'text.Horizontal.TProgressbar',
            [('Horizontal.Progressbar.trough',
              {'children': [('Horizontal.Progressbar.pbar',
                             {'side': 'left', 'sticky': 'ns'})],
               'sticky': 'nswe'}),
             ('Horizontal.Progressbar.label',
              {'sticky': 'nswe'})]
        )
        # self.style_prbr.configure('text.Horizontal.TProgressbar',
        #                           text=self.__text_bar.get(),
        #                           anchor='center')
        self.__progressbarr = ttk.Progressbar(
            self, mode='determinate',
            style='text.Horizontal.TProgressbar',
            variable=self.__value_bar
        )
        self.__progressbarr.grid(column=1, row=9, sticky='ew', columnspan=10,
                                 padx=30, pady=1)
        self.__btn_svd_photo = ttk.Button(self, text='Сохранить фото')
        self.__btn_svd_photo.grid(column=11, row=9, sticky='nsew', padx=10)
        self.__text_editor = ScrolledText(self, height=10, wrap='word')
        self.__text_editor.grid(column=1, row=10, columnspan=11,
                                rowspan=2, sticky='nsew', padx=10, pady=5)

    def display_txt(self, text: str):
        self.__text_editor.insert('end', f'{text}\n')

    def clear_display(self, from_line=('1.0')):
        self.__text_editor.delete(from_line, 'end')

    def get_vk_user_id(self):
        return self.__vk_user_id.get()

    def get_vk_token(self):
        return self.__vk_token.get()

    def get_yd_token(self):
        return self.__yd_token.get()

    def set_albums_box(self, album_names: list[str], v_default=''):
        self.__alb_box.configure(values=album_names)
        self.__alb_box.set(v_default)

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

    def set_progress_bar(self, max_value: float):
        self.__progressbarr.configure(maximum=max_value)

    def make_step_progressbarr(self, value: float):
        self.__value_bar.set(value)
        self.update_idletasks()

    def set_text_bar(self, text=''):
        self.__config_text_prbar(text)
        self.update_idletasks()

    def __config_text_prbar(self, text: str):
        self.style_prbr.configure(
            'text.Horizontal.TProgressbar', text=text, anchor='center'
        )


if __name__ == '__main__':
    window = MyWindow()
    window.mainloop()
