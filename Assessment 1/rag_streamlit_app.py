# -*- coding: utf-8 -*-
"""
RAG Streamlit App – HBR Apple Article Q&A
Uses Chroma + SentenceTransformer + optional local LLM (Ollama + SmolLM).
Deploy: streamlit run rag_streamlit_app.py

For local LLM: Install Ollama from ollama.ai, then run: ollama pull smollm
"""

import os
import streamlit as st
from pathlib import Path

os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "apple_db"
DEFAULT_PDF_PATH = BASE_DIR / "HBR_How_Apple_Is_Organized_For_Innovation-4.pdf"
OLLAMA_MODELS = ["smollm", "mistral"]  # smollm works on low RAM; mistral needs ~4.5GB

st.set_page_config(page_title="RAG – HBR Apple Article", page_icon="📄", layout="centered")

QNA_SYSTEM = """You answer questions using ONLY the provided context. Do not infer, guess, or add information.
- Quote or state only what is explicitly written in the context.
- For "who are the authors": only name people explicitly listed as authors of the article.
- If the exact answer is not clearly in the context, say "I don't know"."""

QNA_TEMPLATE = """###Context
{context}

###Question
{question}"""


@st.cache_resource
def get_embedding_model():
    from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
    return SentenceTransformerEmbeddings(model_name="thenlper/gte-large")


def ollama_available():
    """Check if Ollama is running and model is available."""
    try:
        import ollama
        ollama.list()
        return True
    except Exception:
        return False


def generate_answer_ollama(context: str, question: str, model: str, max_tokens=128, max_context_chars=2500):
    """Limit context length (balance speed vs accuracy)."""
    if len(context) > max_context_chars:
        context = context[:max_context_chars] + "..."
    prompt = QNA_TEMPLATE.format(context=context, question=question)
    full_prompt = QNA_SYSTEM + "\n\n" + prompt
    try:
        import ollama
        r = ollama.generate(model=model, prompt=full_prompt, options={"num_predict": max_tokens})
        return (r.get("response", "") or "").strip()
    except Exception as e:
        return f"LLM error: {e}"


def get_vectorstore(_embedding_model, persist_dir=str(OUT_DIR), document_chunks=None):
    from langchain_community.vectorstores import Chroma
    if document_chunks is None and os.path.exists(persist_dir):
        return Chroma(persist_directory=persist_dir, embedding_function=_embedding_model)
    if document_chunks is not None:
        os.makedirs(persist_dir, exist_ok=True)
        return Chroma.from_documents(
            document_chunks, _embedding_model, persist_directory=persist_dir
        )
    return None


def build_chunks_from_pdf(pdf_path):
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    loader = PyPDFLoader(str(pdf_path))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=20)
    return loader.load_and_split(text_splitter)


def main():
    st.markdown("## HBR Apple Article Q&A")
    st.caption("Document-based Q&A (RAG) — ask questions and get answers from the PDF.")

    with st.sidebar:
        st.subheader("Settings")
        use_existing_db = os.path.exists(OUT_DIR)
        if use_existing_db:
            st.success("Knowledge base is ready.")
        else:
            st.info("Upload a PDF to build the knowledge base.")

        uploaded_file = st.file_uploader("Upload PDF (optional)", type=["pdf"])
        pdf_path = None
        if uploaded_file:
            pdf_path = BASE_DIR / "uploaded_doc.pdf"
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("PDF saved.")
        elif DEFAULT_PDF_PATH.exists():
            pdf_path = DEFAULT_PDF_PATH
            st.caption(f"Using: {DEFAULT_PDF_PATH.name}")

        k_retrieve = st.slider("Sources to retrieve", 1, 5, 4, help="More = better recall (authors, etc.)")
        max_tokens = st.slider("Max answer length (tokens)", 64, 256, 100, help="Lower = faster")
        use_llm = st.checkbox("Use local LLM (Ollama)", value=True)
        ollama_model = st.selectbox("Model", OLLAMA_MODELS, index=0, help="Smollm = low RAM; Mistral needs ~4.5GB")
        if use_llm:
            ollama_ok = ollama_available()
            if ollama_ok:
                st.caption(f"Ollama ready. Pull if needed: ollama pull {ollama_model}")
            else:
                st.caption("Install Ollama, then: ollama pull smollm")

    # Load embedding model
    try:
        embedding_model = get_embedding_model()
    except Exception as e:
        st.error(f"Embedding model failed: {e}")
        st.stop()

    use_ollama = use_llm and ollama_available()

    # Vector store
    document_chunks = None
    if not use_existing_db and pdf_path and pdf_path.exists():
        with st.spinner("Chunking PDF..."):
            document_chunks = build_chunks_from_pdf(pdf_path)
            if not document_chunks:
                st.error("No content from PDF.")
                st.stop()
    vectorstore = get_vectorstore(embedding_model, document_chunks=document_chunks)
    if vectorstore is None:
        st.error("No knowledge base. Upload a PDF in the sidebar.")
        st.stop()

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k_retrieve, "fetch_k": min(k_retrieve + 2, 10)},
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    query = st.chat_input("Ask a question (e.g. Who are the authors?)")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Retrieving..."):
            docs = retriever.invoke(query)
        context = " ".join(d.page_content for d in docs)

        if use_ollama and context.strip():
            with st.spinner("Generating answer..."):
                answer = generate_answer_ollama(context, query, model=ollama_model, max_tokens=max_tokens)
        else:
            answer = context.strip() if context else "No relevant text found."

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        with st.expander("Sources"):
            for i, d in enumerate(docs):
                page = d.metadata.get("page", "?")
                st.markdown(f"**{i+1} (page {page})**")
                st.write(d.page_content[:400] + ("..." if len(d.page_content) > 400 else ""))


if __name__ == "__main__":
    main()
