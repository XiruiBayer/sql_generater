import streamlit as st
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

    # 构造完整的SQL语句
    sql_header = '(' + ', '.join(['{}'] * len(df.iloc[0])) + ')'
    sql_body = ',\n'.join([sql_header.format(*row) for row in sql_rows[1:]])
    full_sql = f"INSERT INTO {Path(filename).stem}\n ({', '.join(sql_rows[0])})\nVALUES\n{sql_body};"
    # print(full_sql)
    # 将full_sql显示在textEdit中
    return full_sql


def main():
    st.set_page_config(layout="wide")
    st.title("SQL Generator")
    uploaded_file = st.file_uploader("Choose CSV", type=['csv'])
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file, header=None)
        st.divider()
        st.write(df)
        filename = uploaded_file.name
        sql = deal(df, filename)
        st.divider()
        st.text(sql)


if __name__ == "__main__":
    main()
