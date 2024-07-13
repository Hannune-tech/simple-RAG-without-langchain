# params for model
embedding_model="text-embedding-ada-002"
language_model="gpt-3.5-turbo"
embedding_batch_size=8

# params for prompt
system_message="You are skilled assistant."

# params for chunking
chunking_method="Semantic" # (Naive, Semantic)
chunk_token_size=256 # Naive
chunk_overlap=0.2 # Naive
min_tokens=64 # Semantic
max_tokens=256 # Semantic
split_window_size=1 # Semantic

# params for DB
top_k=5
chromadb_distance_metric="cosine" # (cosine, l2)
chromadb_collection_name="simple-rag-without-langchain"
