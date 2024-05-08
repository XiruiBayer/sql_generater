import streamlit as st
import pandas as pd
import requests


def deal(bytes_data):
    xls = pd.ExcelFile(bytes_data)
    sheet_names = xls.sheet_names
    sql_list = []
    for sheet in sheet_names:
        sql_tabel_name = pd.read_excel(bytes_data, sheet_name=sheet, nrows=0)
        # print()
        df = pd.read_excel(bytes_data, sheet_name=sheet, header=1)
        col = ''
        for i in df.itertuples():
            col = col + i[1] + ' ' + i[2] + ','
        col = col[:-1]
        sql_create = f'CREATE TABLE {sql_tabel_name.columns.tolist()[0]} ({col});'
        # print(sql_create)
        sql_list.append(sql_create)
    return sql_list




def main():
    st.set_page_config(layout="wide")
    st.title("SQL CREATE Generator")
    excel_filename = "pages/example_2.xlsx"

    try:
        with open(excel_filename, "rb") as file:
            excel_bytes = file.read()

        st.download_button(
            label="Download Example Data",
            data=excel_bytes,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except FileNotFoundError:
        st.error(f"文件 {excel_filename} 未找到，请确保文件存在于应用程序的当前目录。")
    uploaded_file = st.file_uploader("Choose xlsx", type=['xlsx'])
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        filename = uploaded_file.name
        st.divider()
        sql_list = deal(bytes_data)
        for i in sql_list:
            st.text(i)


if __name__ == '__main__':
    main()
