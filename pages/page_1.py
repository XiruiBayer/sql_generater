import streamlit as st
from annotated_text import annotated_text
import pandas as pd
from pathlib import Path


def deal(df, filename):
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
    full_sql = f"""INSERT INTO {Path(filename).stem} \n({(', '.join(header_row)).replace("'", "")}) VALUES\n"""
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
    csv_filename = "pages/example_1.csv"

    try:
        with open(csv_filename, "rb") as file:
            csv_bytes = file.read()

        st.download_button(
            label="Download Example Data",
            data=csv_bytes,
            file_name=csv_filename,
            mime="text/csv"
        )
    except FileNotFoundError:
        st.error(f"文件 {csv_filename} 未找到，请确保文件存在于应用程序的当前目录。")
    uploaded_file = st.file_uploader("Choose CSV", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, header=None)
        st.divider()
        st.write(df)
        filename = uploaded_file.name
        sql = deal(df, filename)
        st.divider()
        st.code(sql, language='sql')


if __name__ == '__main__':
    main()
