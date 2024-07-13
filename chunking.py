import re
import numpy as np
from semantic_router.encoders import OpenAIEncoder
from semantic_router.splitters import RollingWindowSplitter
from helper import transform_dict_n_str
import os
from dotenv import load_dotenv
import config as cfg

load_dotenv()

def set_template():
    template = {
        "document_title": None,
        "document_type": None,
        "content_index": None,
        "content": None,
        "content_index_type": None
    }
    return template

class naive_sentence_chunking:
    def __init__(self, chunk_size=512, overlap=0.2):
        self.chunk_size = chunk_size # max tokens
        self.overlap = overlap


    def start(self, retrieved_text:dict):
        chunked_text_list = []

        template = set_template()
        template["document_title"] = retrieved_text["document_title"]
        template["document_type"] = retrieved_text["document_type"]
        template["content_index_type"] = retrieved_text["contents_index_type"]


        for idx, content in retrieved_text["contents"].items(): 
            if "text" not in content:
                continue
            template["content"] = {}
            template["content_index"] = idx
            chunked_text = ""

            sentences = re.split(r'(?<=\.) |\n', content["text"])
            max_tokens = 0
            total_tokens = 0
            for sentence in sentences:
                total_tokens += len(sentence.split(" "))
                max_tokens = max(max_tokens, len(sentence.split(" ")))   
            for sentence in sentences:
                tokens_in_sentence = sentence.split(" ")
                if len(chunked_text.split(" ")) + len(tokens_in_sentence) < self.chunk_size:
                    chunked_text += sentence + " "
                else:
                    template["content"] = {"text":chunked_text.strip()}
                    chunked_text = sentence
                    chunked_text_list.append(transform_dict_n_str(template, dict_2_str=True))

            template["content"] = {"text":chunked_text.strip()}
            chunked_text_list.append(transform_dict_n_str(template, dict_2_str=True))

        return chunked_text_list
    

class semantic_chunking:
    def __init__(self):
        self.embedding_model = cfg.embedding_model
        self.max_tokens = cfg.max_tokens 
        self.min_tokens = cfg.min_tokens
        self.split_window_size = cfg.split_window_size


    def start(self, retrieved_text:dict):
        encoder = OpenAIEncoder(
            name=self.embedding_model, 
            openai_api_key=os.getenv("CUSTOM_OPENAI_API_KEY"),
        )


        splitter = RollingWindowSplitter(
            encoder=encoder, 
            max_split_tokens=self.max_tokens, 
            min_split_tokens=self.min_tokens,
            window_size=self.split_window_size,
            plot_splits=False,
            enable_statistics=False
        )
        
        template = set_template()
        template["document_title"] = retrieved_text["document_title"]
        template["document_type"] = retrieved_text["document_type"]
        template["content_index_type"] = retrieved_text["contents_index_type"]

        chunked_text_list = []        
        chunked_text = ""
        for idx, content in retrieved_text["contents"].items():
            if "text" not in content:
                continue
            chunked_text += content["text"]
        
        splits = splitter([chunked_text])
        # for chunk in splits:
        for i in range(len(splits)):
            chunk = splits[i]
            chunk = " ".join(chunk.docs)
            template["content"] = {"text":chunk}
            template["content_index"] = i
            chunked_text_list.append(transform_dict_n_str(template, dict_2_str=True))
  
        return chunked_text_list