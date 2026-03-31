import streamlit as st
import traceback

st.title("Debug Mode App")

try:
    import pandas as pd
    import numpy as np
    import io
    from datetime import datetime

    st.success("Semua library berhasil di-load ✅")

    uploaded_files = st.file_uploader(
        "Upload file",
        accept_multiple_files=True
    )

    if uploaded_files:
        st.write("File terdeteksi:", [f.name for f in uploaded_files])

except Exception as e:
    st.error("Terjadi error saat startup:")
    st.text(str(e))
    st.text(traceback.format_exc())
