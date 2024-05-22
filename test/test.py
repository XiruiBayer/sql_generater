import streamlit as st
from streamlitextras.cookiemanager import get_cookie_manager

cookie_manager = None
def main():
    global cookie_manager
    cookie_manager = get_cookie_manager()
    cookie_manager.delayed_init() # Makes sure CookieManager stays in st.session_state

    cookie_manager.set("my_cookie_name", "I'm a cookie!")
    my_cookie_value = cookie_manager.get("my_cookie_name")
    print(my_cookie_value) # "I'm a cookie"

    my_cookies = cookie_manager.get_all()
    print(my_cookies) # {"my_cookie_name": "I'm a cookie!"}

    cookie_manager.delete("my_cookie_name")
    my_cookie_value = cookie_manager.get("my_cookie_name")
    print(my_cookie_value) # None


if __name__ == "__main__":
    main()