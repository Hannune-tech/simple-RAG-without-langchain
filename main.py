import streamlit as st
from dotenv import load_dotenv
from extraction import naive_text_extraction
from chunking import naive_sentence_chunking, semantic_chunking
from models_api import openai_api
import config as cfg
from vector_db import _chromadb
from helper import augment_input
from copy import deepcopy


load_dotenv()
naive_text_extraction = naive_text_extraction()
naive_sentence_chunking = naive_sentence_chunking()
semantic_chunking = semantic_chunking()
model_api = openai_api()

if "chroma_db" not in st.session_state:
    st.session_state["chroma_db"] = _chromadb()


def main():
    # Initialize messages
    if "messages" not in st.session_state:
        set_messages()

    # Add data to the database
    set_db()    
    
    # Chat interface
    chat()
    
    with st.sidebar:
        st.write("***")
        if st.button("Clear chat"):
            set_messages()

        if st.button("Reset "):
            reset()

    
def chat():
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("Ask me anything"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get embeddings for the last user message
        embedding = model_api.embedding([prompt])[0]

        # Retrieve relevant chunks
        relevant_chunks = st.session_state["chroma_db"].retrieve_relevant_chunks(embedding)

        # Augment the input by adding the relevant chunks
        augmented_prompt = augment_input(prompt, relevant_chunks)

        # Temporarily update the last message with the augmented input
        _messages = deepcopy(st.session_state.messages)
        _messages[-1]["content"] = augmented_prompt

        # Generate response with augmented input
        response = model_api.inference(_messages)

        with st.chat_message("assistant"):
            st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def reset():
    for key in st.session_state:
        del st.session_state[key]


def set_messages():
    st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "system", "content": cfg.system_message})


def set_db():
    with st.sidebar:
        st.title("Upload Files")
        docs = st.file_uploader("Choose a file", accept_multiple_files=True)
        
        if st.button("Process"):
            set_messages() # initialize messages whenever new files are uploaded
            st.session_state["chroma_db"].create_collection()
            st.success("New collection created from chroma db")
            with st.spinner("Processing..."):
                for doc in docs:
                    # Extract text
                    output = naive_text_extraction.start(doc)
                    if output is None:
                        st.warning(f"Could not extract text from {doc.name}")
                        continue

                    # Chunk text
                    if cfg.chunking_method == "Naive":
                        output = naive_sentence_chunking.start(output)
                    elif cfg.chunking_method == "Semantic":
                        output = semantic_chunking.start(output)

                    # Get embeddings
                    for i in range(0, len(output), cfg.embedding_batch_size):
                        chunks = output[i:i+cfg.embedding_batch_size]
                        embeddings = model_api.embedding(chunks)

                        # Store texts and embeddings
                        st.session_state["chroma_db"].add_text_and_embedding(chunks, embeddings)
            st.success("Processing complete")
            

if __name__ == "__main__":
    main()