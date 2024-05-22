from datetime import datetime, timedelta
import streamlit as st
from streamlit_cookies_manager import CookieManager
import time


class web_cookie_manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(web_cookie_manager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.cookie_manager = CookieManager()
        # self.cookie_manager._default_expiry = datetime.now() + timedelta(minutes=1)
        if not self.cookie_manager.ready():
            st.stop()

    def set_cookie(self, cookie_name, content):
        self.cookie_manager[cookie_name] = content
        st.session_state[cookie_name] = content
        self.cookie_manager.save()
        time.sleep(0.1)

    def get_cookie(self, cookie_name):
        value = self.cookie_manager.get(cookie_name)
        if value:
            st.session_state[cookie_name] = value
        return value
        # st.write(f"{cookie_name}: {value}")

    def delete_cookie(self, cookie_name):
        value = None
        if cookie_name in self.cookie_manager:
            value = self.cookie_manager.pop(cookie_name)
            st.session_state[cookie_name] = None
        # st.write(f"del: {value}")


cookie_manager = web_cookie_manager()
