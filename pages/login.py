import time
import streamlit as st
from tools.cookie_tools import cookie_manager


def login():
    if not cookie_manager.get_cookie("sql_generator_user"):
        user = st.text_input(label=":pig: 你是谁:", key="username")
        if user:
            cookie_manager.set_cookie("sql_generator_user", user)
            st.switch_page("main.py")
    else:
        st.switch_page("main.py")


if __name__ == '__main__':
    login()
