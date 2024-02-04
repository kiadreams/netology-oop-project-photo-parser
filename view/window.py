from calendar import c
import time
import tkinter as tk
from tkinter import ttk as tkttk
from tkinter.scrolledtext import ScrolledText


class MyWindow(tk.Tk):

    def __init__(self, screenName: str | None = None,
                 baseName: str | None = None,
                 className: str = "Tk",
                 useTk: bool = True,
                 sync: bool = False,
                 use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.geometry('800x400')
        self.title('Приложение резервного копирования фото с VK')
        self.distination = tk.StringVar(value="яндекс")
        self.vk_user_id = tk.StringVar(value='')
        self.vk_token = tk.StringVar(value='')
        self.yd_token = tk.StringVar(value='')
        self.__crt_btn_svd_photo()
        self.__crt_alb_combox()
        self.__crt_progressbar()
        self.__set_grid()
        self.__crt_label_album()
        self.__crt_label_photo()
        self.__crt_spinbox_nums_ph()
        self.__crt_label_vk_user_id()
        self.__crt_entr_vk_id()
        self.__crt_label_vk_token()
        self.__crt_entr_vk_token()
        self.__crt_label_yd_token()
        self.__crt_entr_yd_token()
        self.__crt_label_distinat()
        self.__crt_radbtn_distinat_1()
        self.__crt_text_editor()
        # self.__crt_radbtn_distinat_2() # Пока не готово

    def __set_grid(self):
        for i in range(1, 11):
            self.rowconfigure(index=i, weight=1)
            self.columnconfigure(index=i, weight=1)
        self.rowconfigure(index=11, weight=4)
        self.columnconfigure(index=11, weight=1)

    def __crt_btn_svd_photo(self):
        self.btn_svd_photo = tkttk.Button(self, text='Сохранить фото')
        self.btn_svd_photo.grid(column=11, row=9)

    def __crt_alb_combox(self):
        self.alb_box = tkttk.Combobox(self)
        self.alb_box.grid(column=1, row=6, columnspan=2)

    def __crt_progressbar(self):
        self.progressbarr = tkttk.Progressbar(self)
        self.progressbarr.grid(column=1, row=9, sticky='ew',
                               columnspan=10,
                               padx=30, pady=1)
    
    def __crt_label_album(self):
        self.__label_album = tkttk.Label(self, text='ВЫБЕРИТЕ АЛЬБОМ')
        self.__label_album.grid(column=1, row=5, columnspan=2)

    def __crt_label_photo(self):
        self.__label_photo = tkttk.Label(
            self,
            text='кол-во фото\n(" " копировать все)'
            )
        self.__label_photo.grid(column=3, row=5)
    
    def __crt_spinbox_nums_ph(self):
        values = ['5', 'все']
        self.spinbox_photo = tkttk.Spinbox(self, values=values, wrap=True,
                                           justify='center')
        self.spinbox_photo.set(values[0])
        self.spinbox_photo.grid(column=3, row=6, sticky='w')
    
    def __crt_label_vk_user_id(self):
        self.__label_vk_user_id = tkttk.Label(
            self,
            text='Введите user id\n пользователя VK'
            )
        self.__label_vk_user_id.grid(column=1, row=1)
    
    def __crt_entr_vk_id(self):
        self.entr_vk_id = tkttk.Entry(self, textvariable=self.vk_user_id)
        self.entr_vk_id.grid(column=2, row=1, columnspan=2, sticky='ew',
                             padx=10)

    def __crt_label_vk_token(self):
        self.__label_vk_token = tkttk.Label(
            self,
            text='Введите ключ доступа\n к аккаунту VK'
            )
        self.__label_vk_token.grid(column=4, row=1)
    
    def __crt_entr_vk_token(self):
        self.entr_vk_token = tkttk.Entry(self, textvariable=self.vk_token)
        self.entr_vk_token.grid(column=5, row=1, columnspan=7, sticky='nsew',
                                padx=10, pady=10)

    def __crt_label_yd_token(self):
        self.__label_yd_token = tkttk.Label(
            self,
            text='Введите ключ доступа\n к вашему яндекс ДИСКУ'
            )
        self.__label_yd_token.grid(column=1, row=2)
    
    def __crt_entr_yd_token(self):
        self.entr_yd_token = tkttk.Entry(self, textvariable=self.yd_token)
        self.entr_yd_token.grid(column=2, row=2, columnspan=3, sticky='nsew',
                                padx=10, pady=10)

    def __crt_label_distinat(self):
        self.__label_distance = tkttk.Label(self, text='Куда копировать')
        self.__label_distance.grid(column=9, row=6, columnspan=2)
    
    def __crt_radbtn_distinat_1(self):
        self.radbtn_distinat_1 = tkttk.Radiobutton(self, text='Яндекс ДИСК',
                                                   value='яндекс',
                                                   variable=self.distination)
        self.radbtn_distinat_1.grid(column=9, row=7, columnspan=2,
                                    sticky='nsew', padx=10, pady=10)

    def __crt_radbtn_distinat_2(self):
        self.radbtn_distinat_2 = tkttk.Radiobutton(self, text='Google ДИСК',
                                                   value='google',
                                                   variable=self.distination)
        self.radbtn_distinat_2.grid(column=9, row=8, columnspan=2,
                                    sticky='nsew', padx=10, pady=10)

    def __crt_text_editor(self):
        self.text_editor = ScrolledText(self, height=10)
        self.text_editor.grid(column=1, row=10, columnspan=11,
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



