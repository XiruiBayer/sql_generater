import streamlit as st
from annotated_text import annotated_text
import pandas as pd
import pyperclip


def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Copy Success!")


def deal_excel(excel_bytes):
    xls = pd.ExcelFile(excel_bytes)
    sheet_names = xls.sheet_names
    sql_list = []
    for sheet in sheet_names:
        sql_tabel_name = pd.read_excel(excel_bytes, sheet_name=sheet, nrows=0)
        sql_tabel_name = sql_tabel_name.columns.tolist()[0]
        # print()
        df = pd.read_excel(excel_bytes, sheet_name=sheet, header=0)
        sql_list.append(deal_sheet(df, sql_tabel_name))
    return sql_list, df


def deal_sheet(df, tablename):
    # 初始化SQL语句的主体
    sql_rows = []
    for index, row in df.iterrows():
        # 初始化每行数据的SQL片段
        sql_row = []
        for value in row:
            # 处理NULL值和字符串值，避免数据类型错误
            if pd.isna(value):
                sql_value = "NULL"
            elif isinstance(value, str):
                value = value.replace("''", "'")
                value = value.replace("'", "''")
                sql_value = f"'{value}'"
            else:
                sql_value = str(value)  # 数值类型直接转换为字符串，不加单引号
            sql_row.append(sql_value)
        # 将每行数据的SQL片段加入到总SQL中
        sql_rows.append(tuple(sql_row))
    # print(sql_rows)
    header_row = sql_rows[0]
    body_rows = sql_rows[1:]
    # 构造完整的SQL语句
    full_sql = f"""INSERT INTO {tablename} \n({(', '.join(header_row)).replace("'", "")}) VALUES\n"""
    # print(full_sql)
    sql_body = ''
    for body in body_rows:
        sql_body += f"""({",".join(body)}),\n"""
    sql_body = sql_body.rstrip(",\n") + ";"
    return full_sql + sql_body


def main():
    st.set_page_config(layout="wide")
    st.title("SQL INSERT Generator")
    annotated_text(
        ("README", ""),
        "    The name of the incoming CSV file will be recognized as the table name.",
    )
    # 指定你想要提供下载的Excel文件名
    excel_filename = "static/example_1.xlsx"
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
    all_sql = ''
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        filename = uploaded_file.name
        sql_list, df = deal_excel(bytes_data)
        st.divider()
        all_sql = '\n'.join(sql_list)
        if st.button('Copy all SQL'):
            copy_to_clipboard(all_sql)
        for sql in sql_list:
            st.code(sql, language='sql')


if __name__ == '__main__':
    main()
