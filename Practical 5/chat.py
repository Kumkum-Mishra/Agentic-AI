from langchain_google_genai import ChatGoogleGenerativeAI
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
	raise ValueError("Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment or .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, google_api_key=api_key)

prompt = "tell me a joke on programming"

response = llm.invoke(prompt)

print(response.content)