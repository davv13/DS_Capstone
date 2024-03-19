import os
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

api_key_path = 'openai_api_key.txt'
try:
    with open(api_key_path, 'r') as f:
        os.environ["OPENAI_API_KEY"] = f.read().strip()
except FileNotFoundError:
    st.error(f"API key file '{api_key_path}' not found. Please make sure the file exists.")
    st.stop()

PERSIST = False
DATA_DIRECTORY = "data/"

st.set_page_config(page_title='Bank Information Retrieval Assistant')

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

query_text = st.text_input("", placeholder="Ask a question...", key="query")

submit = st.button('Submit')

if submit and query_text:
    query_result = index.query(query_text)
    
    st.session_state.chat_history.append(("You:", query_text))
    st.session_state.chat_history.append(("Bot:", query_result))
    
    st.experimental_rerun()

for message_type, message_text in st.session_state.chat_history:
    st.text_area(label="", value=f"{message_type} {message_text}", height=75, key=message_text[:20], disabled=True)