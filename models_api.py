"""
All the code related to LLM models will be done here.
text-generation/embedding

"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import config as cfg


load_dotenv()


class openai_api:
    def __init__(self):
        self.client = self.initialize_openai_api()


    def initialize_openai_api(self):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return client


    def inference(self, message):
        model_name = cfg.language_model

        completion = self.client.chat.completions.create(
            model=model_name,
            messages=message
        )
        response = completion.choices[0].message.content
        return response


    def embedding(self, text_list):
        model_name = cfg.embedding_model

        embedding_results = self.client.embeddings.create(model=model_name, input=text_list)
        embedding_results = embedding_results.data
        embedding_results = [embedding_result.embedding for embedding_result in embedding_results]
        return embedding_results
