from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)


def local_fallback_reply(user_text):
    text = user_text.lower()
    if "interstellar" in text:
        return (
            "Interstellar is about a team of astronauts who travel through a wormhole to find "
            "a new home for humanity because Earth is dying. The movie mixes family emotions, "
            "space science, and the idea that love and time are deeply connected."
        )
    if "inception" in text:
        return (
            "Inception follows a thief who enters dreams to steal ideas, but is asked to plant "
            "an idea instead. The story moves through multiple dream layers where time runs at "
            "different speeds."
        )
    if "matrix" in text:
        return (
            "The Matrix is about a hacker who discovers reality is a computer simulation and joins "
            "a rebellion to free humanity."
        )
    return (
        "I could not call the online model right now, so this is an offline fallback response. "
        "Try a movie question like Interstellar, Inception, or The Matrix."
    )


chat_history = []
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    chat_history.append(HumanMessage(content=user_input))
    try:
        response = llm.invoke(chat_history)
        assistant_text = response.content
    except Exception:
        assistant_text = local_fallback_reply(user_input)

    chat_history.append(AIMessage(content=assistant_text))
    print(f"Assistant: {assistant_text}")

print(chat_history)