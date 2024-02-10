from view.controller import Controller
# from security.get_token import TOKEN_VK, TOKEN_YD, CLIENT_ID_VK


app = Controller()

# VK token получал с 'scope': 6.

# app.window._MyWindow__vk_token.set(TOKEN_VK)
# app.window._MyWindow__yd_token.set(TOKEN_YD)
# app.window._MyWindow__vk_user_id.set(CLIENT_ID_VK)

app.window.mainloop()
