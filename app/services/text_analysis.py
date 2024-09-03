import json
import time

import chromadb
from chromadb.api.models.Collection import Collection
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from .ai_integration import call_model, query_similar_chunks, create_embeddings, generate_embeddings

chroma_client = chromadb.PersistentClient(path="/Users/mor.iluz/Desktop/chroma")



def analyze_document(content, prompt):
    collection: Collection = chroma_client.create_collection(name=f"collection_{int(time.time())}")
    chunks = split_content(content)

    print(f"Generate and save embeddings for collection {collection.name}")
    embeddings = create_embeddings(collection, chunks)
    #todo compute_average_embedding(embeddings)

    #langchain
    # embedding_function = OpenAIEmbeddings()
    # db = Chroma(embedding_function=embedding_function)
    # db.similarity_search(query="tell me about monday soc 2 report")
    #
    # query = generate_embeddings("Summarize the key points about SOC2 controls")
    # query_result = collection.query(query_embeddings=query, n_results=5)
    #

    similar_chunks = query_similar_chunks(collection, embeddings)
    #combined_text = " ".join(chunk['text'] for chunk in similar_chunks)

    print("Summarize report using model")
    insights = call_model(similar_chunks, prompt)
    insights_dict = json.loads(insights)

    return json.dumps(insights_dict, indent=2)


def split_content(content, max_tokens=2000):
    paragraphs = content.split("\n\n")
    chunks = []
    current_chunk = []
    current_token_count = 0

    for paragraph in paragraphs:
        token_count = len(paragraph.split())
        if current_token_count + token_count > max_tokens:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [paragraph]
            current_token_count = token_count
        else:
            current_chunk.append(paragraph)
            current_token_count += token_count

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks
