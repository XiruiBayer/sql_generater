import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")
from streamlit_navigation_bar import st_navbar
import pages as pg
from pathlib import Path


functions = {
    "Home": pg.show_home,
    "CREATE": pg.show_create,
    "INSERT": pg.show_insert,
}

pages = ["Home", "CREATE", "INSERT"]
styles = styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "left",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
options = {
    "show_menu": False,
    "show_sidebar": True,
    "use_padding": True,
}
logo = Path(__file__).parent / "static" / "logo.svg"
page = st_navbar(
    pages,
    # logo_path=str(logo),
    styles=styles,
    options=options,
)
go_to = functions.get(page)
if go_to:
    go_to()