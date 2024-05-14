from utils import *
from sql_generator import *


def deal(bytes_data):
    xls = pd.ExcelFile(bytes_data)
    sheet_names = xls.sheet_names
    sql_list = []
    for sheet in sheet_names:
        sql_tabel_name = pd.read_excel(bytes_data, sheet_name=sheet, nrows=0)
        df = pd.read_excel(bytes_data, sheet_name=sheet, header=1)
        col = ''
        for i in df.itertuples():
            col = f"{col}{i[1]} {i[2]},\n"
        col = col[:-1]
        sql_create = f'CREATE TABLE {sql_tabel_name.columns.tolist()[0]} \n({col});'
        sql_list.append(sql_create)
    return sql_list


def main():
    st.set_page_config(layout="wide")
    st.title("SQL CREATE Generator")
    st.markdown("""
        #####  README:
        + Support generating SQL simultaneously from multiple sheets inputted.
        + Modifying the data displayed in the DataFrame results in real-time updates to the underlying SQL.
    """)
    download_button(Path("static/example_2.xlsx"), 'xlsx')
    uploaded_file = st.file_uploader("Choose xlsx", type=['xlsx'])

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        sql_generator = SqlGenerator(bytes_data)
        st.text('')
        sql_generator.show_create_sql()


if __name__ == '__main__':
    main()
