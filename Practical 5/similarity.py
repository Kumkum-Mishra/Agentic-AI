from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
	raise ValueError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment or .env file.")

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=api_key)


docs=["Apple is fruit","Apple is a company","Banana is a fruit"]

query="Apple fruit"

doc_embeddings = embeddings.embed_documents(docs)
query_embedding = embeddings.embed_query(query)

similarities = cosine_similarity([query_embedding], doc_embeddings)

print(similarities)