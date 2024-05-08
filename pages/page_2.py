import streamlit as st
import pandas as pd
from pathlib import Path


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
            # print(i[1])  # 字段名称
            # print(i[2])  # 字段类型
        col = col[:-1]
        sql_create = f'CREATE TABLE {sql_tabel_name.columns.tolist()[0]} ({col});'
        # print(sql_create)
        sql_list.append(sql_create)
    return sql_list


def main():
    st.set_page_config(layout="wide")
    st.title("SQL Generator")
    uploaded_file = st.file_uploader("Choose CSV", type=['xlsx'])
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        # df = pd.read_csv(uploaded_file, header=None)
        bytes_data = uploaded_file.getvalue()
        # st.divider()
        # st.write(df)
        filename = uploaded_file.name
        st.divider()
        sql_list = deal(bytes_data)
        for i in sql_list:
            st.text(i)

if __name__ == '__main__':
    main()