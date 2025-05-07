from sklearn.metrics.pairwise import cosine_similarity
from src.open_api_client import get_openai_client
import numpy as np
import pandas as pd

def main():
    client = get_openai_client()

    # Define text inputs
    text_1 = "What is Retrieval-Augmented Generation?"
    text_2 = "How do you use external data with language models?"
    text_3 = "Schedule a sync for Friday at 3 PM."

    # Generate embeddings
    embedding_1 = get_embedding_for_text(text_1, client)
    embedding_2 = get_embedding_for_text(text_2, client)
    embedding_3 = get_embedding_for_text(text_3, client)

    # Store embeddings in a dictionary
    embedding_store = {
        "RAG Overview": embedding_1,
        "External Data Use": embedding_2,
        "Meeting Schedule": embedding_3
    }

    # Create a query embedding
    query_text = "Tell me about data retrieval methods."
    query_embedding = get_embedding_for_text(query_text, client)

    # Compare query with each stored document
    for title, emb in embedding_store.items():
        score = calculate_cosine_similarity(query_embedding, emb)
        print(f"Similarity with '{title}': {score:.4f}")

    # Create a DataFrame from embeddings
    documents = pd.DataFrame({
        "title": list(embedding_store.keys()),
        "embedding": [np.array(r.data[0].embedding) for r in embedding_store.values()]
    })
    query_vector = np.array(query_embedding.data[0].embedding)
    documents["similarity"] = documents["embedding"].apply(lambda emb: cosine_similarity([query_vector], [emb])[0][0])

    # Retrieve the most relevant document
    top_doc = documents.sort_values("similarity", ascending=False).iloc[0]
    print(f"Top match for the query: {top_doc['title']}")

def calculate_cosine_similarity(response1, response2):
    embedding1 = np.array(response1.data[0].embedding)
    embedding2 = np.array(response2.data[0].embedding)
    return cosine_similarity([embedding1], [embedding2])[0][0]

def get_embedding_for_text(text: str, client):
    response = client.embeddings.create( input=text, model="text-embedding-ada-002" )
    return response


if __name__ == '__main__':
    main()