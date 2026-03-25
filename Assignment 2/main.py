import google.generativeai as genai
import os

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from dotenv import load_dotenv
import os

load_dotenv()  # load .env file

api_key = os.getenv("GOOGLE_API_KEY")

import google.generativeai as genai
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")

# ---------------- Tools ----------------
search = DuckDuckGoSearchRun()
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# ---------------- Agent ----------------
def research_agent(topic):

    print("🔍 Searching web...")
    web_data = search.run(topic)

    print("📚 Searching Wikipedia...")
    wiki_data = wiki.run(topic)

    combined_data = (web_data + "\n\n" + wiki_data)[:2000]

    prompt = f"""
You are an expert research assistant.

Create a structured report on: {topic}

Use this information:
{combined_data}

FORMAT:

COVER PAGE
Title: {topic}

INTRODUCTION (5 lines)

KEY FINDINGS (bullet points)

CHALLENGES (bullet points)

FUTURE SCOPE (bullet points)

CONCLUSION (4 lines)

IMPORTANT:
- Do not repeat text
- Keep it clean and professional
"""

    response = model.generate_content(prompt)

    return response.text

topic = "Climate Change Impact"

report = research_agent(topic)

print("\n===== FINAL REPORT =====\n")
print(report)

# Save file
with open("report.txt", "w", encoding="utf-8") as f:
    f.write(report)
