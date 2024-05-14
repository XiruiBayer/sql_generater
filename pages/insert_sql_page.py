from utils import *
from sql_generator import *

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
        st.info(f"Modify and preview your SQLs")
        sql_generator.show_insert_sql()
        if "SQL" in st.session_state:
            st.success("All SQLs Ready")
            with st.expander("Expand to Copy All"):
                st.code(st.session_state.SQL)


if __name__ == '__main__':
    main()
