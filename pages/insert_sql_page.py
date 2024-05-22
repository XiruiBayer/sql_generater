import streamlit as st
# st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

from tools.sql_generator import SqlGenerator
from tools.utils import download_button, multi_columns, Login
from pathlib import Path


def show_insert():
    Login.check_login()
    Login.log_out_button()
    st.title("SQL INSERT Generator")
    st.markdown("""
        #####  README:
        + Support generating SQL simultaneously from multiple sheets inputted.
        + Modifying the data displayed in the DataFrame results in real-time updates to the underlying SQL.
    """)
    download_button(Path("static/example_1.xlsx"), 'xlsx')
    # 获取用户输入
    st.header('Add Global Columns', divider='rainbow')
    st.session_state.num_input = st.number_input("Add Quality", min_value=1, max_value=12, value=1)
    # 根据用户输入动态显示列
    multi_columns(st.session_state.num_input)
    st.header('Upload File', divider='rainbow')
    uploaded_file = st.file_uploader("Choose xlsx", type=['xlsx'])
    st.header('Show Result', divider='rainbow')
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        sql_generator = SqlGenerator(bytes_data)
        st.text('')
        st.info(f"In this block, preview and make real-time modifications to the Dataframe and SQL queries.")
        sql_generator.show_insert_sql()
        if "SQL" in st.session_state:
            # st.success("All SQLs Ready")
            with st.expander(":point_down: In this block, preview and copy all SQL statements. :point_down: "):
                st.code(st.session_state.SQL)


if __name__ == '__main__':
    show_insert()
