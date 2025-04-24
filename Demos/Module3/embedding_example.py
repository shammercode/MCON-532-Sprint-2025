from src.open_api_client import get_openai_client
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

client = get_openai_client()

event_descriptions = [
    "Midterm project demo for Data Structures on March 15th at 2 PM.",
    "Weekly group meeting for Operating Systems lab every Thursday.",
    "Final exam review session for Algorithms with Prof. Lin.",
    "Office hours with TA for Machine Learning, Tuesday 11 AM.",
    "Hackathon planning meeting for ACM student chapter.",
    "Seminar on AI safety and ethics this Friday.",
    "Dentist appointment Thursday April 14 at 2PM.",
    "Deadline for submission of Research Paper Proposal.",
    "Workshop on Git and GitHub basics for new CS majors.",
    "Presentation on distributed systems project, Room 302."
]

def get_embedding_for_text(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response

def calculate_cosine_similarity(response1, response2):
    embedding1 = np.array(response1.data[0].embedding)
    embedding2 = np.array(response2.data[0].embedding)
    return cosine_similarity([embedding1], [embedding2])[0][0]

def main():
    print("Event Descriptions:")
    for idx, event in enumerate(event_descriptions, 1):
        print(f"{idx}. {event}")

    print("\nGenerating embeddings...")
    embeddings = [get_embedding_for_text(event) for event in event_descriptions]

    print("Calculating cosine similarities...\n")
    similarity_matrix = np.zeros((len(event_descriptions), len(event_descriptions)))

    for i in range(len(event_descriptions)):
        for j in range(i + 1, len(event_descriptions)):
            similarity = calculate_cosine_similarity(embeddings[i], embeddings[j])
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity

    # Set diagonal to 1.0 since cosine similarity of any vector with itself is 1
    np.fill_diagonal(similarity_matrix, 1.0)

    # Set pandas display options to avoid truncation
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    index_labels = [str(i + 1) for i in range(len(event_descriptions))]
    df_similarity = pd.DataFrame(similarity_matrix, columns=index_labels, index=index_labels)

    print("Cosine Similarity Matrix:")
    print(df_similarity)

if __name__ == "__main__":
    main()
