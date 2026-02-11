# -*- coding: utf-8 -*-
"""
RAG Streamlit App – Live UI for the same RAG pipeline as Final_Copy_Mini_Project_4.ipynb
Uses: HBR document (PDF), Chroma, SentenceTransformer (gte-large), Mistral-7B (llama-cpp).
"""

import os
import streamlit as st
from pathlib import Path

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="RAG – HBR Apple Article",
    page_icon="📄",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Paths (same as notebook: apple_db, optional PDF path)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "apple_db"
DEFAULT_PDF_PATH = BASE_DIR / "HBR_How_Apple_Is_Organized_For_Innovation-4.pdf"

# ---------------------------------------------------------------------------
# Load dependencies once (cached)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_embedding_model():
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
    return SentenceTransformerEmbeddings(model_name="thenlper/gte-large")


def get_vectorstore(_embedding_model, persist_dir=str(OUT_DIR), document_chunks=None):
    """Load Chroma from persist_dir if it exists and no new chunks; else build from chunks."""
    from langchain_community.vectorstores import Chroma
    if document_chunks is None and os.path.exists(persist_dir):
        return Chroma(persist_directory=persist_dir, embedding_function=_embedding_model)
    if document_chunks is not None:
        os.makedirs(persist_dir, exist_ok=True)
        return Chroma.from_documents(
            document_chunks,
            _embedding_model,
            persist_directory=persist_dir,
        )
    return None


def build_chunks_from_pdf(pdf_path):
    """Same as notebook: PyPDFLoader + RecursiveCharacterTextSplitter (512, 20)."""
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    loader = PyPDFLoader(str(pdf_path))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=20,
    )
    return loader.load_and_split(text_splitter)


# ---------------------------------------------------------------------------
# Prompts (same as notebook)
# ---------------------------------------------------------------------------
QNA_SYSTEM_MESSAGE = """
You are an assistant whose work is to review the report and provide the appropriate answers from the context.
User input will have the context required by you to answer user questions.
This context will begin with the token: ###Context.
The context contains references to specific portions of a document relevant to the user query.

User questions will begin with the token: ###Question.

Please answer only using the context provided in the input. Do not mention anything about the context in your final answer.

If the answer is not found in the context, respond "I don't know".
"""

QNA_USER_MESSAGE_TEMPLATE = """
###Context
Here are some documents that are relevant to the question mentioned below.
{context}

###Question
{question}
"""


def generate_rag_response(user_input, retriever, llm, k=2, max_tokens=256, temperature=0, top_p=0.95, top_k=50):
    """Same logic as notebook: retrieve → build prompt → LLM."""
    relevant_document_chunks = retriever.invoke(user_input)
    context_list = [d.page_content for d in relevant_document_chunks]
    context_for_query = ". ".join(context_list)
    user_message = QNA_USER_MESSAGE_TEMPLATE.format(context=context_for_query, question=user_input)
    prompt = QNA_SYSTEM_MESSAGE.strip() + "\n" + user_message
    try:
        response = llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        return f"Sorry, I encountered the following error:\n{e}"


# ---------------------------------------------------------------------------
# LLM: llama-cpp (same as notebook) – optional; can be disabled for UI-only demo
# ---------------------------------------------------------------------------
@st.cache_resource
def get_llm(model_path=None, download_if_missing=True):
    """Load Mistral-7B via llama-cpp. Set model_path or allow download from HuggingFace."""
    if model_path and os.path.exists(model_path):
        from llama_cpp import Llama
        return Llama(model_path=model_path, verbose=False)
    if download_if_missing:
        try:
            from huggingface_hub import hf_hub_download
            path = hf_hub_download(
                repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
                filename="mistral-7b-instruct-v0.2.Q6_K.gguf",
            )
            from llama_cpp import Llama
            return Llama(model_path=path, verbose=False)
        except Exception as e:
            st.warning(f"LLM load failed (need model file or HF): {e}. You can still use retrieval-only.")
            return None
    return None


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
def main():
    st.title("RAG – HBR: How Apple Is Organized for Innovation")
    st.caption("Same pipeline as notebook: PDF → Chunk → Embed (gte-large) → Chroma → Retriever → Mistral-7B")

    # Sidebar: PDF / Vector store setup
    with st.sidebar:
        st.subheader("Document & vector store")
        use_existing_db = os.path.exists(OUT_DIR)
        if use_existing_db:
            st.success(f"Using existing Chroma DB: `{OUT_DIR}`")
        else:
            st.info("No `apple_db` found. Run the notebook once to create it, or upload a PDF below.")
        uploaded_file = st.file_uploader("Or upload PDF to build index (optional)", type=["pdf"])
        pdf_path = None
        if uploaded_file:
            pdf_path = BASE_DIR / "uploaded_doc.pdf"
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("PDF saved. Building vector store on first query.")
        elif DEFAULT_PDF_PATH.exists():
            pdf_path = DEFAULT_PDF_PATH
            st.caption(f"Default PDF: `{DEFAULT_PDF_PATH.name}`")

    # Load embedding model
    try:
        embedding_model = get_embedding_model()
    except Exception as e:
        st.error(f"Embedding model load failed: {e}")
        st.stop()

    # Vector store: existing DB or build from PDF
    document_chunks = None
    if not use_existing_db and pdf_path and pdf_path.exists():
        with st.spinner("Chunking and embedding PDF..."):
            document_chunks = build_chunks_from_pdf(pdf_path)
            if not document_chunks:
                st.error("No chunks from PDF.")
                st.stop()
    vectorstore = get_vectorstore(embedding_model, document_chunks=document_chunks)
    if vectorstore is None:
        st.error("No vector store. Run the notebook to create `apple_db` or upload a PDF.")
        st.stop()

    # Sidebar: retrieval and LLM
    k_retrieve = st.sidebar.slider("Retrieval k", 1, 5, 2)
    max_tokens = st.sidebar.slider("Max tokens", 64, 512, 256)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k_retrieve})

    use_llm = st.sidebar.checkbox("Use LLM (Mistral-7B via llama-cpp)", value=True)
    llm = None
    if use_llm:
        custom_path = st.sidebar.text_input("Custom GGUF model path (optional)", "")
        llm = get_llm(model_path=custom_path if custom_path else None)

    # Main: query
    query = st.text_input("Ask a question about the HBR document", placeholder="e.g. Who are the authors of this article?")

    if query:
        # Retrieval (always)
        with st.spinner("Retrieving..."):
            docs = retriever.invoke(query)
        st.subheader("Retrieved chunks")
        for i, d in enumerate(docs):
            with st.expander(f"Chunk {i+1} (page {d.metadata.get('page', '?')})"):
                st.text(d.page_content[:500] + ("..." if len(d.page_content) > 500 else ""))

        # Generation (if LLM loaded)
        if llm:
            with st.spinner("Generating answer..."):
                answer = generate_rag_response(query, retriever, llm, k=k_retrieve, max_tokens=max_tokens)
            st.subheader("Answer")
            st.write(answer)
        else:
            st.info("Enable 'Use LLM' and ensure the model is available for generated answers.")


if __name__ == "__main__":
    # Run: streamlit run rag_streamlit_app.py
    # Ensure notebook was run once to create apple_db, or place PDF in this folder / upload in app.
    main()
