from utils import *
from sql_generator import *
from functools import partial


def main():
    st.set_page_config(layout="wide")
    st.title("SQL INSERT Generator")
    st.markdown("""
        #####  README:
        + Support generating SQL simultaneously from multiple sheets inputted.
        + Modifying the data displayed in the DataFrame results in real-time updates to the underlying SQL.
    """)
    download_button(Path("static/example_1.xlsx"), 'xlsx')
    uploaded_file = st.file_uploader("Choose xlsx", type=['xlsx'])
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        sql_generator = SqlGenerator(bytes_data)
        st.text('')
        if st.button(":sparkles: COPY ALL SQL :sparkles:", on_click=partial(copy_sql_action)):
            st.success("Copy Success!")
        sql_generator.show_insert_sql()


if __name__ == '__main__':
    main()
