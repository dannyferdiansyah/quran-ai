import streamlit as st
from google.api_core import retry
from dotenv import load_dotenv
# Importing palm, retry functions, and other dependencies
import google.generativeai as palm
import os

# Load environment variables from .env file
load_dotenv()

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY")
palm.configure(api_key=api_key)

# Function to retry chat with exponential backoff
@retry.Retry()
def retry_chat(**kwargs):
    return palm.chat(**kwargs)

# Function to retry reply with exponential backoff
@retry.Retry()
def retry_reply(arg):
    return palm.reply(arg)

def is_quran_related(response):
    # Lakukan pengecekan di sini, misalnya:
    # Jika response berisi kata-kata terkait Al-Qur'an, kembalikan True; jika tidak, kembalikan False
    # Misalnya, Anda dapat melakukan pemfilteran berdasarkan konteks yang spesifik terkait Al-Qur'an
    if "Quran" in response:
        return True
    return False

# Streamlit app
def main():
    st.set_page_config(page_title="Qur'anAI", page_icon="ngaji.png")
    st.image("icon.png", width=350)  # Logo or icon
    st.write(
        """
        Welcome to Qur'anAI, an AI-powered tool to search for words in Al-Qur'an.
        """
    )
    st.title("Search Words (Latin) in Al-Qur'an")
    st.markdown("---")

    # Get available models
    models = [m.name for m in palm.list_models() if 'generateMessage' in m.supported_generation_methods]

    # Model selection dropdown
    selected_model = st.selectbox("Select model :", models)
    st.markdown("---")
    
    # Default question text
    default_question = "I need to know the words Work available in Al-Qur'an. Can you tell me what Surah, Ayat and Translation?"

    # Input for user question
    question = st.text_area("Ask a words containts in Al-Qur'an:", value=default_question, height=300)

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    if st.button("Submit"):
        if question:
            # Retry chat interaction
            response = retry_chat(
                model=selected_model,
                context="You are a professional Quran Reciter and good at searching words in Quran.",
                messages=question,
            )

            # Memeriksa apakah respons terkait Al-Qur'an
            if is_quran_related(response.last):  # Menggunakan fungsi is_quran_related dengan response.last
                # Menampilkan respons hanya jika terkait Al-Qur'an
                st.text("Response:")
                st.write(response.last)
                st.session_state.conversation_history.append(f"{question}")
            else:
                st.text("Response not related to Al-Qur'an.")

    st.sidebar.title("History")
    for entry in st.session_state.conversation_history:
        st.sidebar.text(entry)

    if st.sidebar.button('Clear History'):
        st.session_state.conversation_history = []
        
if __name__ == "__main__":
    main()