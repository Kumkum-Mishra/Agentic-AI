from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
st.header("Movie Summary Generator")


movie_input=st.selectbox("Select a movie:", ["Inception", "The Matrix", "Interstellar"])
style_input=st.selectbox("Select an explanation style:", ["concise", "detailed", "narrative"])
length_input=st.selectbox("Select explanation length:", ["short", "medium", "long"])

template = PromptTemplate(
    template="""
Please summarize the movie titled "{movie_input}".

Explanation Style: {style_input}  
Explanation Length: {length_input}  

- Clearly explain the plot, themes, and main characters.
- Mention important cinematic or storytelling elements if relevant.
- Use simple analogies to explain complex ideas.

If required information is unavailable, respond with:
"Insufficient information available"

Ensure the summary is accurate and aligned with the given style and length.
""",
input_variables=["movie_input", "style_input","length_input"],validate_template=True
)


prompt=template.invoke({
    "movie_input": movie_input,
    "style_input": style_input,
    "length_input": length_input
})


# user_input = st.text_input("Enter your prompt here:")

if st.button("Submit"):
    try:
        response = model.invoke(prompt)
        st.write(response.content)
    except Exception:
        st.warning("Gemini quota/API unavailable. Showing offline fallback response.")
        st.write(
            f"Offline fallback ({style_input}, {length_input}): {movie_input} is summarized with "
            "focus on plot, key characters, and themes. Retry later for live Gemini output."
        )
