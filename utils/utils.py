from pathlib import Path
import streamlit as st


def download_button(fine_path: Path, file_type: str) -> None:
    try:
        with open(fine_path, "rb") as file:
            excel_bytes = file.read()
        if file_type == 'xlsx':
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            st.error(f"file_type: {file_type}.Unsupported file type.")
        st.download_button(
            label="Download Example Data",
            data=excel_bytes,
            file_name=fine_path.name,
            mime=mime_type
        )
    except FileNotFoundError:
        st.error(f"file: {fine_path}.No such file or directory.")


def multi_columns(num_cols):
    # 确保num_cols在合理范围内
    num_rows = min(max(num_cols, 1), 10)
    seen_values = set()  # 用来存储所有已输入的col1的值
    st.session_state.not_process = []
    for row in range(num_rows):
        # 每行创建三个columns
        col1, col2, col3 = st.columns(3)
        # 在当前行的columns中添加内容
        actual_index = row * 3
        with col1:
            user_input = st.text_input(':rainbow[add key]', value="", placeholder="insert_user", key=str(actual_index + 1))
            # 检查输入是否重复
            if user_input in seen_values:
                st.session_state.not_process.append(row)
                st.error("This value has been used before!", icon="🚨")
            else:
                seen_values.add(user_input)  # 如果值不重复，则添加到集合中
                st.session_state[f'text_input_{row}_1'] = user_input
        with col2:
            st.session_state[f'text_input_{row}_2'] = st.text_input(':rainbow[add value]', value="", placeholder="xirui",
                                                                    key=str(actual_index + 2))
        with col3:
            st.session_state[f'text_input_{row}_3'] = st.toggle("Force", value=False, key=str(actual_index + 3))
            if st.session_state[f'text_input_{row}_3']:
                st.write("Ignore existing data and forcibly replace it with additional value!")





def multi_column_bak(num_cols):
    # 确保num_cols在合理范围内
    num_cols = min(max(num_cols, 1), 10)
    # 计算需要的行数
    num_rows = -(-num_cols // 3)  # 向上取整除法计算所需行数
    for row in range(num_rows):
        # 每行创建三个columns
        cols_in_row = st.columns(3)

        # 在当前行的columns中添加内容
        for i, col in enumerate(cols_in_row):
            # 计算当前column对应的实际索引
            actual_index = row * 3 + i
            if actual_index < num_cols:
                title = col.text_input("Movie title", f"Life of {actual_index}", key=f"input_{actual_index}")
            else:
                # 如果实际索引超出用户输入的列数，可以不添加任何内容或显示占位符
                pass
