import pandas as pd
import streamlit as st
from utils.sql_builder import escape_string
from uuid import uuid4
from copy import deepcopy
from io import BytesIO


class SqlGenerator:
    def __init__(self, file: bytes):
        self.file = file
        self.table_content = self.convert_sheet2df()

    def convert_sheet2df(self) -> dict:
        file = BytesIO(self.file)
        xls = pd.ExcelFile(file)
        sheet_names = xls.sheet_names
        table_content = {}
        for sheet in sheet_names:
            file = BytesIO(self.file)
            sql_tabel_name = pd.read_excel(file, sheet_name=sheet, nrows=0).columns.tolist()[0]
            converters = {col: str for col in
                          pd.read_excel(file, sheet_name=sheet, header=1, nrows=1).columns.tolist()}
            df = pd.read_excel(file, sheet_name=sheet, header=1, converters=converters)
            df.index = df.index + 1
            table_content[sql_tabel_name] = df
        return table_content

    def show_insert_sql(self) -> None:
        insert_sql = ''
        tabs = st.tabs(self.table_content.keys())

        for i, tab in enumerate(tabs):
            df = self.fill_additional_key(list(self.table_content.values())[i])
            edited_df = tab.data_editor(df, hide_index=True,
                                        use_container_width=True, key=uuid4())
            sql = self.df2sql_insert(edited_df, list(self.table_content.keys())[i])
            tab.code(sql)
            insert_sql += f"{sql}\n\n"
        st.session_state.SQL = insert_sql

    def df2sql_insert(self, data_df, table_name) -> str:
        data_df = self.fill_additional_key(data_df)
        table_columns = data_df.columns
        sql = f"INSERT INTO {table_name}\n({','.join(table_columns)}) VALUES"
        # deal body
        for index, row in data_df.iterrows():
            sql_row = []
            for value in row:
                if not value:
                    sql_value = "NULL"
                elif pd.isna(value):
                    sql_value = "NULL"
                elif isinstance(value, str):
                    if value.endswith(" 00:00:00"):
                        value = value[:-9]
                        # print(value)
                    value = escape_string(value)
                    sql_value = f"'{value}'"
                else:
                    sql_value = str(value)
                sql_row.append(sql_value)
            sql = f"{sql}\n({','.join(sql_row)}),"
        sql = f"{sql[:-1]};"
        return sql


    @staticmethod
    def fill_additional_key(data_df) -> pd.DataFrame:
        table_columns = data_df.columns.tolist()
        for i in range(st.session_state.num_input):
            if i in st.session_state.not_process:
                continue
            input_key = st.session_state[f"text_input_{i}_1"]
            input_value = st.session_state[f"text_input_{i}_2"]
            force_update = st.session_state[f"text_input_{i}_3"]
            # Check if the key already exists in the DataFrame
            if input_key in table_columns:
                add_key_index = table_columns.index(input_key)
                # Modify rows based on force_update flag
                table_contents = [
                    (row.tolist()[:add_key_index] +
                     ([input_value] if force_update or not row.tolist()[add_key_index] else [row.tolist()[add_key_index]]) +
                     row.tolist()[add_key_index + 1:])
                    for _, row in data_df.iterrows()
                ]
            elif input_key:  # Key doesn't exist and has a non-empty value
                table_columns.append(input_key)
                # Append value to each row
                table_contents = [
                    row + ([input_value] if input_value else [None])
                    for row in data_df.values.tolist()
                ]
            # Update DataFrame with modified contents and columns
            if 'table_contents' in locals():  # Ensure table_contents was defined in the loop
                data_df = pd.DataFrame(table_contents, columns=table_columns)

        return data_df

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
