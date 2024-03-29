import os
import uuid
import streamlit as st

from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import DirectoryLoader
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

st.set_page_config(page_title='Bank Information Retrieval Assistant')

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except FileNotFoundError:
    api_key = os.getenv('OPENAI_API_KEY')

headers = {
    "authorization": api_key
}

if not api_key:
    st.error("API key not found. Please set it as an environment variable or in secrets.toml.")
    st.stop()

PERSIST = False
DATA_DIRECTORY = "data/"

st.markdown("""
    <style>
        .reportview-container .main .block-container {
            padding-top: 5rem;
        }
        h1 {
            text-align: center;
            position: relative;
            color: #FFF;
        }
        .chatbox-container {
            position: fixed;
            bottom: 5rem;
            left: 50%;
            transform: translate(-50%, 0);
            width: 90%;
        }
        /* New CSS for the chat text */
        .chat-message {
            color: white;
            background-color: #333;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .chat-input {
            color: white;
            background-color: #333;
            border-radius: 5px;
            padding: 10px;
            margin-top: 20px;
        }
    </style>
    <h1>Bank Information Retrieval Assistant</h1>
""", unsafe_allow_html=True)


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if PERSIST and os.path.exists("persist"):
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader(DATA_DIRECTORY)
    index = VectorstoreIndexCreator().from_loaders([loader])

def submit_query():
    if st.session_state.query_text:
        query_result = index.query(st.session_state.query_text)
        
        st.session_state.chat_history.append(("You:", st.session_state.query_text))
        st.session_state.chat_history.append(("Bot:", query_result))

if 'query_text' not in st.session_state:
    st.session_state['query_text'] = ""

query_text = st.text_input("", placeholder = "Ask a question...", key="query_text", on_change=submit_query)

submit = st.button('Submit', on_click=submit_query)

for message_type, message_text in st.session_state.chat_history:
    st.text_area(label="", value=f"{message_type} {message_text}", height=75, key=uuid.uuid4(), disabled=True)