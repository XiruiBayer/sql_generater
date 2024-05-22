import streamlit as st

# st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

from tools.utils import download_button, Login
from pathlib import Path
from tools.sql_generator import SqlGenerator


def show_create():
    Login.check_login()
    Login.log_out_button()
    st.title("SQL CREATE Generator")
    st.markdown("""
        #####  README:
        + Support generating SQL simultaneously from multiple sheets inputted.
        + Modifying the data displayed in the DataFrame results in real-time updates to the underlying SQL.
    """)
    download_button(Path("static/example_2.xlsx"), 'xlsx')
    st.header('Upload File', divider='rainbow')

    uploaded_file = st.file_uploader("Choose xlsx", type=['xlsx'])
    st.header('Show Result', divider='rainbow')

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        sql_generator = SqlGenerator(bytes_data)
        st.text('')
        st.info(f"In this block, preview and make real-time modifications to the Dataframe and SQL queries.")
        sql_generator.show_create_sql()
        if "SQL" in st.session_state:
            with st.expander(":point_down: In this block, preview and copy all SQL statements. :point_down:"):
                st.code(st.session_state.SQL)


if __name__ == '__main__':
    show_create()
