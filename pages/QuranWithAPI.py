import streamlit as st
import requests

def cari_kata_arab(arti):
    base_url = "https://api.alquran.cloud/search/{query}/all/id.indonesian"
    url = base_url.format(query=arti)

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        hasil_pencarian = data['data']['matches']

        if hasil_pencarian:
            for hasil in hasil_pencarian:
                kata_arab = hasil['text']
                surah_name = hasil['surah']['name']
                ayat = hasil['numberInSurah']
                st.write(f"Kata Arab: {kata_arab}")
                st.write(f"Arti: {arti}")
                st.write(f"Surah: {surah_name}, Ayat: {ayat}\n")
        else:
            st.warning("Maaf, kata tidak ditemukan dalam kamus.")
    else:
        st.error("Terjadi kesalahan dalam melakukan permintaan.")

# Tampilan antarmuka Streamlit
st.set_page_config(page_title="Qur'anAPI", page_icon="../FIX/ngaji.png")
st.image("../FIX/icon.png", width=350)  # Logo or icon
st.title("Search Words (Latin) in Al-Qur'an")
st.markdown("---")

kata_dicari = st.text_input("Masukkan arti kata dalam Bahasa Indonesia")
st.markdown("---")

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if st.button("Cari"):
    if kata_dicari:
        cari_kata_arab(kata_dicari)
        st.session_state.conversation_history.append(f"{kata_dicari}")
    else:
        st.warning("Masukkan arti kata terlebih dahulu.")

st.sidebar.title("History")
for entry in st.session_state.conversation_history:
    st.sidebar.text(entry)

if st.sidebar.button('Clear History'):
    st.session_state.conversation_history = []