import sys
from pathlib import Path

tools_path = Path(__file__).parent / 'tools'
if tools_path not in sys.path:
    sys.path.append(str(tools_path))

import streamlit as st

from tools.utils import Login
from tools.cookie_tools import cookie_manager


def show_home():
    Login.log_out_button()
    user = cookie_manager.get_cookie("sql_generator_user")
    if not user:
        st.switch_page(Login.LOGIN_PAGE)
    else:
        st.title(f"Hello {user}!")
    # st.page_link("pages/home.py", label="Home", icon="🏠")
    # st.page_link("pages/insert_sql_page.py", label="INSERT SQL Generator", icon="1️⃣")
    # st.page_link("pages/create_sql_page.py", label="CREATE SQL Generator", icon="2️⃣")


if __name__ == '__main__':
    show_home()
