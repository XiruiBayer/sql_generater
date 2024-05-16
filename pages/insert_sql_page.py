from utils.utils import *
from utils.sql_generator import *


def main():
    st.set_page_config(layout="wide")
    st.title("SQL INSERT Generator")
    st.markdown("""
        #####  README:
        + Support generating SQL simultaneously from multiple sheets inputted.
        + Modifying the data displayed in the DataFrame results in real-time updates to the underlying SQL.
    """)
    download_button(Path("static/example_1.xlsx"), 'xlsx')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.text_input_1 = st.text_input('additional key', value="", placeholder="insert_user")
    with col2:
        st.session_state.text_input_2 = st.text_input('additional value', value="", placeholder="xirui")
    with col3:
        st.session_state.text_input_3 = st.toggle("Force", value=False)
        if st.session_state.text_input_3:
            st.write("Ignore existing data and forcibly replace it with additional data!")
    uploaded_file = st.file_uploader("Choose xlsx", type=['xlsx'])
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
    main()
