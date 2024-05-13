import pandas as pd
import streamlit as st


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
            df = pd.read_excel(self.file, sheet_name=sheet, header=1)
            df.index = df.index + 1
            table_content[sql_tabel_name] = df
        return table_content

    def show_insert_sql(self):
        insert_sql = ''
        for table_name, df in self.table_content.items():
            st.divider()
            # deal header
            df = st.data_editor(df,hide_index=True,use_container_width=True)
            table_columns = df.columns
            sql = f"INSERT INTO {table_name}\n({','.join(table_columns)}) VALUES"
            # deal body
            for index, row in df.iterrows():
                sql_row = []
                for value in row:
                    if pd.isna(value):
                        sql_value = "NULL"
                    elif isinstance(value, str):
                        value = value.replace("''", "'")
                        value = value.replace("'", "''")
                        sql_value = f"'{value}'"
                    else:
                        sql_value = str(value)
                    sql_row.append(sql_value)
                sql = f"{sql}\n({','.join(sql_row)})"
            st.code(sql)
            insert_sql += sql
        st.session_state.SQL = insert_sql

    def show_create_sql(self):
        create_sql = ''
        for table_name, df in self.table_content.items():
            st.divider()
            df = st.data_editor(df,hide_index=True,use_container_width=True)
            col = ''
            for i in df.itertuples():
                col = f"{col}{i[1]} {i[2]},\n"
            col = col[:-2]
            sql = f'CREATE TABLE {table_name} \n({col});'
            st.code(sql)
            create_sql += "{sql}\n"
        st.session_state.SQL = create_sql


if __name__ == '__main__':
    s = SqlGenerator('static/example_1.xlsx')
    print(s.get_insert_sql())
