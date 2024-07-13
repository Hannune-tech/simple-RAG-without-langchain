import json
import streamlit as st


def transform_dict_n_str(_input, dict_2_str=True):
    if dict_2_str:
        _output = json.dumps(_input, ensure_ascii=False)
    else: # str 2 dict
        _output = json.loads(_input)
    return _output


def augment_input(prompt, relevant_chunks):
    distances = relevant_chunks.pop("distances")[0]
    documents = relevant_chunks.pop("documents")[0]

    relevant_chunks = "\n".join([f"distance: {str(distances[i])}, text:{documents[i]}" for i in range(len(documents))])

    integrated_prompt = f"""
The following process involves Retrieval-Augmented Generation (RAG). Based on the initial prompt provided below, relevant text chunks have been retrieved to aid in generating a comprehensive response.

Initial Prompt:
"{prompt}"

Retrieved Relevant Chunks:
{relevant_chunks}

Using the initial prompt and the relevant chunks provided, please generate a detailed and informative response.
    """

    return integrated_prompt