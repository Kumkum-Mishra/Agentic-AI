from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

messages = [
    SystemMessage(content="You are a helpful assistant that provides movie summaries."),
    HumanMessage(content="Can you summarize the movie Inception?")
]

try:
    response = llm.invoke(messages)
    assistant_text = response.content
except Exception:
    assistant_text = (
        "Offline fallback summary: Inception is about Dom Cobb, a skilled extractor who enters "
        "people's dreams to steal secrets. He gets a chance to clear his past if he can perform "
        "inception, planting an idea inside someone's mind, across layered dream worlds."
    )

messages.append(AIMessage(content=assistant_text))
print(messages)