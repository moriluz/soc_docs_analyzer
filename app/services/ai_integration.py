import chromadb
import numpy as np
from chromadb.api.models.Collection import Collection
from openai import OpenAI

chroma_client = chromadb.Client()
client = OpenAI()

def call_model(chunk, prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": f"Analyze the following SOC 2 documentation and provide insights: {chunk}"}
        ]
    )
    return response.choices[0].message.content


def create_embeddings(collection: Collection, chunks):
    embeddings = []
    for idx, chunk in enumerate(chunks):
        embedding = generate_embeddings(chunk)
        collection.add(
            embeddings=embedding,
            documents=chunk,
            ids=idx.__str__()
            # metadatas (file name?)
        )
        embeddings.append(embedding)

    return embeddings


def generate_embeddings(text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )

    return response.data[0].embedding


def query_similar_chunks(collection, embedding):
    response = collection.query(query_embeddings=embedding, n_results=5)

    return response


#check - to summarize or query based on the general content of the document,
#compute the average of the embeddings of all
# the chunks to create a query_embedding that represents the whole document.
def compute_average_embedding(embeddings):
    avg_embedding = np.mean(embeddings, axis=0)
    return avg_embedding