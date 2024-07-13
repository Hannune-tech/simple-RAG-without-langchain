import chromadb
import config as cfg
import uuid


class _chromadb:
    def __init__(self):
        self.client = self.initialize_chromadb()


    def initialize_chromadb(self):
        return chromadb.Client()
    

    def create_collection(self):
        existing_collections = self.client.list_collections()
        if cfg.chromadb_collection_name in [col.name for col in existing_collections]:
            self.client.delete_collection(name=cfg.chromadb_collection_name)
        self.client.create_collection(name=cfg.chromadb_collection_name, distance_metric=cfg.chromadb_distance_metric)


    def create_collection(self):
        existing_collections = self.client.list_collections()
        if cfg.chromadb_collection_name in [col.name for col in existing_collections]:
            self.client.delete_collection(name=cfg.chromadb_collection_name)
        self.collection = self.client.create_collection(
            name=cfg.chromadb_collection_name, 
            metadata={"hnsw:space": cfg.chromadb_distance_metric}
        )


    def add_text_and_embedding(self, text_chunks, embeddings):
        ids = [str(uuid.uuid4()) for _ in range(len(text_chunks))]
        self.collection.add(
            ids=ids,
            documents=text_chunks,
            embeddings=embeddings,
        )


    def retrieve_relevant_chunks(self, vector):   
        return self.collection.query(
            query_embeddings=[vector],
            n_results=cfg.top_k,
        )