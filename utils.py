from pathlib import Path
import streamlit as st
import pyperclip


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
            file_name=fine_path.stem,
            mime=mime_type
        )
    except FileNotFoundError:
        st.error(f"file: {fine_path}.No such file or directory.")


def copy_sql_action():
    if "SQL" in st.session_state:
        pyperclip.copy(st.session_state.SQL)
