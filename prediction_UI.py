import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="Telang-AI",
    page_icon="🧪",
    layout="centered"
)
API_URL = "https://telang-ai-api-945218795183.asia-southeast2.run.app/predict"

def main():
    st.title("🧪 Telang-AI")
    st.markdown("Prediksi pH larutan menggunakan ekstrak Bunga Telang")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nama Sampel")
    with col2:
        desc = st.text_input("Deskripsi Singkat")
    # --- File Uploader untuk Gambar ---
    uploaded_file = st.file_uploader(
        "Pilih gambar larutan",
        type=["jpg", "jpeg", "png"],
        help="Format yang didukung: JPG, JPEG, PNG"
    )
    # --- Tampilkan Gambar yang Diunggah ---
    image_placeholder = st.empty()
    if uploaded_file is not None:
        try:
            # Tampilkan gambar sebagai pratinjau
            image = Image.open(uploaded_file)
            image_placeholder.image(
                image,
                caption="Gambar yang diunggah.",
                use_column_width=True
            )
        except Exception as e:
            st.error(f"Gagal memuat gambar: {e}")
    st.markdown("---")
    # --- Tombol Prediksi ---
    if st.button("🚀 Prediksi pH", use_container_width=True):
        # Validasi input
        if uploaded_file is not None and name and desc:
            with st.spinner('Menganalisis gambar dan mengirim ke server...'):
                try:
                    # Siapkan data untuk dikirim ke API
                    uploaded_file.seek(0)
                    files = {
                        'img': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    payload = {'name': name, 'desc': desc}
                    # Kirim request POST ke API
                    response = requests.post(
                        API_URL, files=files, data=payload, timeout=30)
                    # Periksa status response
                    if response.status_code == 200:
                        result = response.json()
                        ph_value = result.get('pH_value', 'N/A')
                        st.success(
                            f"**Prediksi Berhasil!** Nilai pH adalah: **{ph_value}**")
                    else:
                        error_detail = response.json().get('detail', 'Terjadi kesalahan tidak diketahui.')
                        st.error(
                            f"Gagal mendapatkan prediksi (Error {response.status_code}): {error_detail}")
                except requests.exceptions.RequestException as e:
                    st.error(
                        f"Gagal terhubung ke API. Pastikan Anda terhubung ke internet. Detail: {e}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
        else:
            st.warning(
                "Mohon isi semua field (Nama, Deskripsi) dan unggah gambar terlebih dahulu.")

if __name__ == "__main__":
    main()
