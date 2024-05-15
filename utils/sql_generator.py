import pandas as pd
import streamlit as st
from utils.sql_builder import escape_string
from uuid import uuid4


class SqlGenerator:
    def __init__(self, file: bytes):
        self.file = file
        self.table_content = self.convert_sheet2df()

    def convert_sheet2df(self) -> dict:
        xls = pd.ExcelFile(self.file)
        sheet_names = xls.sheet_names
        table_content = {}
        for sheet in sheet_names:
            sql_tabel_name = pd.read_excel(self.file, sheet_name=sheet, nrows=0).columns.tolist()[0]
            converters = {col: str for col in
                          pd.read_excel(self.file, sheet_name=sheet, header=1, nrows=1).columns.tolist()}
            df = pd.read_excel(self.file, sheet_name=sheet, header=1, converters=converters)
            df.index = df.index + 1
            table_content[sql_tabel_name] = df
        return table_content

    def show_insert_sql(self) -> None:
        insert_sql = ''
        tabs = st.tabs(self.table_content.keys())
        for i, tab in enumerate(tabs):
            edited_df = tab.data_editor(list(self.table_content.values())[i], hide_index=True,
                                        use_container_width=True, key=uuid4())
            sql = self.df2sql_insert(edited_df, list(self.table_content.keys())[i])
            tab.code(sql)
            insert_sql += f"{sql}\n\n"
        st.session_state.SQL = insert_sql

    @staticmethod
    def df2sql_insert(data_df, table_name):
        table_columns = data_df.columns
        sql = f"INSERT INTO {table_name}\n({','.join(table_columns)}) VALUES"
        # deal body
        for index, row in data_df.iterrows():
            sql_row = []
            for value in row:
                if pd.isna(value):
                    sql_value = "NULL"
                elif isinstance(value, str):
                    if value.endswith(" 00:00:00"):
                        value = value[:-9]
                        print(value)
                    value = escape_string(value)
                    sql_value = f"'{value}'"
                else:
                    sql_value = str(value)
                sql_row.append(sql_value)
            sql = f"{sql}\n({','.join(sql_row)}),"
        sql = f"{sql[:-1]};"
        return sql

    def show_create_sql(self):
        create_sql = ''
        tabs = st.tabs(self.table_content.keys())
        for i, tab in enumerate(tabs):
            edited_df = tab.data_editor(list(self.table_content.values())[i], hide_index=True,
                                        use_container_width=True, key=uuid4())

            sql = self.df2sql_create(edited_df, list(self.table_content.keys())[i])
            tab.code(sql)
            create_sql += f"{sql}\n\n"
        st.session_state.SQL = create_sql

    @staticmethod
    def df2sql_create(data_df, table_name):
        col = ''
        for i in data_df.itertuples():
            col = f"{col}{i[1]} {i[2]},\n"
        col = col[:-2]
        sql = f'CREATE TABLE {table_name} \n({col});'
        return sql


if __name__ == '__main__':
    print(uuid4())
