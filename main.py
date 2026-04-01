import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

st.set_page_config(page_title="Merge Komplain", layout="wide")

st.title("📊 Merge & Processing Data Komplain")

uploaded_files = st.file_uploader(
    "Upload file Excel / HTML",
    type=["xls", "xlsx", "html"],
    accept_multiple_files=True
)

processed_dfs = []

if uploaded_files:
    st.info(f"{len(uploaded_files)} file diupload. Processing...")

    for file in uploaded_files:
        try:
            content = file.read()
            df = None

            # Detect HTML
            is_html = False
            try:
                decoded = content.decode("utf-8")
                if decoded.strip().lower().startswith("<html") or \
                   "xmlns:x=\"urn:schemas-microsoft-com:office:excel\"" in decoded.lower():
                    is_html = True
            except:
                pass

            # Read file
            if is_html:
                st.write(f"📄 {file.name} → HTML")
                df = pd.read_html(io.StringIO(decoded))[0]
            else:
                st.write(f"📄 {file.name} → Excel")
            
                if file.name.endswith(".xls"):
                    df = pd.read_excel(io.BytesIO(content), header=None, engine="xlrd")
                else:
                    df = pd.read_excel(io.BytesIO(content), header=None, engine="openpyxl")

            # Set header
            new_header = df.iloc[0]
            df = df[1:]

            # Make unique columns
            cols = new_header.tolist()
            seen = {}
            unique_cols = []

            for col in cols:
                col = str(col)
                count = seen.get(col, 0)
                if count > 0:
                    unique_cols.append(f"{col}_{count}")
                else:
                    unique_cols.append(col)
                seen[col] = count + 1

            df.columns = unique_cols
            processed_dfs.append(df)

        except Exception as e:
            st.error(f"Error di {file.name}: {e}")

    if processed_dfs:
        merged_df = pd.concat(processed_dfs, ignore_index=True)

        # =====================
        # TYPE CONVERSION
        # =====================

        date_cols = ['Tgl Kejadian', 'Tgl Lapor']
        for col in date_cols:
            merged_df[col] = pd.to_datetime(merged_df[col], format='%d/%m/%y', errors='coerce')
        

        time_cols = ['Jam Kejadian', 'Jam Lapor']
        for col in time_cols:
            merged_df[col] = pd.to_datetime(
                merged_df[col],
                errors='coerce'
            ).dt.time

        numeric_cols = ['Rupiah Argo', 'Argo Dibayar', 'Jumlah Komplain', 'Akumulasi Point']
        for col in numeric_cols:
            merged_df[col] = (
                merged_df[col]
                .astype(str)
                .str.replace(r'[^\d.]', '', regex=True)
            )
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

        # =====================
        # TAMBAHAN KOLOM
        # =====================

        merged_df['Tanggal penarikan data CRC'] = (
    pd.Timestamp.now(tz='Asia/Jakarta')
    .tz_localize(None)
    .strftime('%d/%m/%Y %H:%M:%S')
)

        merged_df['Bulan'] = (
    merged_df['Tgl Lapor']
    .dt.to_period('M')
    .dt.to_timestamp()
    .dt.strftime('%d/%m/%Y')
)

        merged_df['Tanggal'] = merged_df['Tgl Lapor'].dt.day

        kategori_mapping = {
            'Route/Arah/Putar2/Tdk Tahu Jalan': 'Route/Arah/Putar2/Tdk Tahu Jalan',
            'Tidak Sopan/Marah2/Komunikasi': 'Tidak Sopan/Marah2/Komunikasi',
            'Mengendarai Tdk Nyaman/Ngebut': 'Mengendarai Tdk Nyaman/Ngebut',
            'Kebersihan': 'Kebersihan'
        }

        merged_df['Kategori'] = merged_df['Sub Jenis Komplain']
        merged_df['Kategori'] = merged_df['Kategori'].where(
            merged_df['Kategori'].isin(kategori_mapping.keys()),
            merged_df['Jenis Komplain']
        )
        merged_df['Kategori'] = merged_df['Kategori'].replace(kategori_mapping)
        merged_df['Kategori'] = merged_df['Kategori'].str.upper()

        for col in date_cols:
            merged_df[col] = merged_df[col].dt.strftime('%d/%m/%Y')

        # =====================
        # OUTPUT
        # =====================

        st.success("✅ Data berhasil diproses!")

        st.subheader("Preview Data")
        st.markdown(f"Total Komplain: {len(merged_df)}")
        st.dataframe(merged_df, use_container_width=True)

        # COPYABLE TABLE
        st.subheader("Copy Data (CSV)")
        csv_data = merged_df.to_csv(index=False)
        st.text_area("Copy di sini:", csv_data, height=200)

        # DOWNLOAD
        output = io.BytesIO()
        merged_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="⬇️ Download Excel",
            data=output,
            file_name="merged_data_komplain.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.warning("Tidak ada data yang berhasil diproses.")
else:
    st.info("Silakan upload file terlebih dahulu.")
