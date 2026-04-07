from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
st.title("Movie Summary generator")
user_input=st.text_input("Enter the name of the movie")
if st.button("Generate Summary"):
    try:
        response = model.invoke(user_input)
        st.write(response.content)
    except Exception:
        st.warning("Gemini quota/API unavailable. Showing offline fallback response.")
        st.write(
            "Offline fallback: This movie explores major characters, central conflict, and the "
            "main theme. For best quality, retry when your Gemini free-tier quota resets."
        )
