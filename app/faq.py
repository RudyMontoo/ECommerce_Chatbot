import os
import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

from groq import Groq
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# Fix: pointing to the actual CSV file
faqs_path = Path(__file__).parent / "resources" / "faq.csv"
chroma_client= chromadb.Client()
client = Groq()
collection_name_faq = "faqs"

ef=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def ingest_faq_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(path)
    
    if collection_name_faq not in chroma_client.list_collections():
        print("Ingesting FAQ data into Chromadb...")
        collection = chroma_client.get_or_create_collection(
            name=collection_name_faq,
            embedding_function=ef
            
        )
        
        docs=df['question'].tolist()
        metadata=[{'answer': ans}for ans in df['answer'].tolist()]
        ids=[f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
    else:
        print(f"Collection {collection_name_faq} already exists.")
    
    return df
    

def get_relevant_qa(query):
    collection =chroma_client.get_or_create_collection(name=collection_name_faq)
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results

def faq_chain(query):
    result=get_relevant_qa(query)
    context=''.join([r.get('answer') for r in result['metadatas'][0]])
    answer=generate_answer(query,context)
    return answer

def generate_answer(query,context):
    prompt=f"""Given the question and context below, generate the answer based on the context only.
    If you don't find the answer inside the context, say "I don't know",
    Do not make things up or invent answers.
    Question: {query}
    Context: {context}
    Answer:
    """
    chat_completion = client.chat.completions.create(
    model=os.environ['GROQ_MODEL'],
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
    )
    return chat_completion.choices[0].message.content
    
if __name__ == '__main__':
    print(faqs_path)
    
    # Testing the ingestion
    try:
        df = ingest_faq_data(faqs_path)
        print("Successfully loaded dataframe with shape:", df.shape)
    except Exception as e:
        print(f"Error loading CSV: {e}")

    query="What's your policy on defective products?"
    # results=get_relevant_qa(query)
    
    answer=faq_chain(query)
    print("Answer:", answer)