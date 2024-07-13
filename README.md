# Simple-RAG-without-LangChain

A straightforward implementation of Retrieval-Augmented Generation (RAG) using Streamlit, without the need for LangChain.

## Overview

This project demonstrates how to implement a simple RAG system to enhance the generation of responses by retrieving relevant text chunks from a corpus. Supported file formats for upload include PDF, PPTX, and DOCX.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/simple-RAG-without-langchain.git
    cd simple-RAG-without-langchain
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Obtain an OpenAI API key from the [OpenAI website](https://openai.com/index/openai-api/).

4. Add your OpenAI API key to a `.env` file in the project directory:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run main.py
    ```

2. Configure parameters as needed by modifying the `config.py` file.

## Workflow

1. **Upload Files**: Upload your documents (PDF, PPTX, DOCX) through the Streamlit interface.
2. **Text Extraction**: Extract text content from the uploaded files.
3. **Text Chunking**: Break down the extracted text into manageable chunks.
4. **Vector Representation**: Convert text chunks into vector representations and store them in a vector database.
5. **Semantic Search**: Perform semantic searches to retrieve relevant text chunks.
6. **Prompt Augmentation**: Augment the prompt with retrieved text chunks.
7. **Generation**: Generate responses based on the augmented prompt.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
