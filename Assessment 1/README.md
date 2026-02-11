# RAG (Retrieval-Augmented Generation) Question Answering System

## 📋 Project Overview

This is a simplified Retrieval-Augmented Generation (RAG) system built with Streamlit, LangChain, and Chroma. It allows you to upload documents (PDFs) and ask questions that are answered using the content from those documents.

**Key Features:**
- 🚀 Simple, single-file Streamlit app
- 🔍 Semantic search with Chroma vector store
- 🧠 Sentence-Transformer embeddings (lightweight)
- 💾 Persistent vector database
- 📱 Beautiful chat interface
- 🎛️ Configurable retrieval settings

---

## 🎯 Problem Statement

Traditional search engines return documents, but users want **direct answers** to their questions. This RAG system:
1. **Retrieves** relevant document chunks based on semantic similarity
2. **Augments** the LLM prompt with retrieved context
3. **Generates** accurate, grounded answers (no hallucinations)

**Example Use Case:** Upload an HBR article about Apple's innovation strategy, then ask questions like:
- "How is Apple organized for innovation?"
- "What are the key principles mentioned?"
- "Who are the decision makers?"

---

## 📊 Architecture

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ Embedding Model      │  (SentenceTransformer: gte-large)
│ Convert Q to vector  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Vector Store         │  (Chroma - Persistent DB)
│ Find top-k chunks    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Retrieved Context    │  (Most relevant document chunks)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ LLM (Optional)       │  (Generate answer with context)
│ Build Answer         │  (Fallback: Display context)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ User Gets Answer     │
└──────────────────────┘
```

---

## 📚 Dataset & Knowledge Source

- **Type:** PDF documents (text-based)
- **Source:** User-uploaded or pre-placed in the project directory
- **Default:** `HBR_How_Apple_Is_Organized_For_Innovation-4.pdf` (HBR Article)
- **Storage:** `apple_db/` directory (Chroma vector database)

---

## 🔧 Text Chunking Strategy

| Parameter | Value | Reason |
|-----------|-------|--------|
| **Chunk Size** | 512 characters | Balances context size with specificity |
| **Chunk Overlap** | 20 characters | Ensures no lost context at boundaries |
| **Separators** | `\n\n`, `\n`, space | Respects document structure |

**Why this strategy?**
- 512 chars ≈ 100-150 words (good semantic units)
- Small overlap prevents information loss
- Recursive splitting preserves paragraph structure

---

## 🧬 Embedding Details

| Component | Details |
|-----------|---------|
| **Model** | `thenlper/gte-large` |
| **Type** | Sentence-Transformer (open-source) |
| **Dimensions** | 1024 |
| **Why This Model?** | Lightweight, fast, excellent semantic quality, no API key needed |

**Alternative Models:**
- `all-MiniLM-L6-v2` (faster but lower quality)
- OpenAI embeddings (paid)
- HuggingFace hosted inference

---

## 💾 Vector Database

| Property | Value |
|----------|-------|
| **Store** | Chroma (persistent) |
| **Location** | `apple_db/` folder |
| **Search Type** | Similarity or MMR (configurable) |
| **Advantages** | No external DB needed, SQLite backend, easy deployment |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Step 1: Clone/Navigate to Project
```bash
cd "k:\GitHub\Agentic-AI\Assessment 1"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Using venv
python -m venv venv
source venv/Scripts/activate  # On Windows

# Or using conda
conda create -n rag-env python=3.10
conda activate rag-env
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Your PDF
Place your PDF in the project directory, or upload via the Streamlit UI.

### Step 5: Run the App
```bash
streamlit run app_simple.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Notebook Implementation

The original Jupyter notebook (`Final_Copy_Mini_Project_4.ipynb`) contains:

1. **Data Loading** - Load PDF and explore content
2. **Chunking** - Split into semantic chunks (512 chars, 20 overlap)
3. **Embedding** - Convert chunks to vectors using gte-large
4. **Vector Store** - Store in Chroma DB
5. **Retrieval** - Semantic similarity search
6. **Generation** - Optional LLM answer generation (Mistral-7B)
7. **Testing** - 3+ test queries with outputs

The Streamlit app (`app_simple.py`) simplifies this to a single, deployable file.

---

## 🧪 Test Queries

### Query 1: General Understanding
**Q:** "How is Apple organized for innovation?"  
**Expected:** Answer about organizational structure, cross-functional teams, decision-making process

### Query 2: Specific Details
**Q:** "What are the key principles of Apple's organization?"  
**Expected:** Answer with specific principles mentioned in the article

### Query 3: People/Leaders
**Q:** "Who leads the innovation process at Apple?"  
**Expected:** Answer about key decision makers and leaders mentioned

---

## 🛠️ Configuration

Open the Streamlit sidebar to configure:

- **Number of Sources (k):** How many document chunks to retrieve (1-10)
- **Search Type:** Similarity (exact match) or MMR (diverse results)
- **Max Answer Length:** Token limit for generated responses
- **Temperature:** Creativity level (0 = focused, 2 = creative)

---

## 📈 Future Improvements

1. **Better Chunking**
   - Semantic chunking (chunk by topic)
   - Sliding window chunks
   - Hierarchical chunking

2. **Reranking / Hybrid Search**
   - Add BM25 (keyword) + semantic search
   - Use cross-encoder reranker (e.g., BAAI/bge-reranker)
   - Ensemble retrieval

3. **Metadata Filtering**
   - Add timestamps, categories, sources
   - Filter by date, author, source document
   - Tag-based retrieval

4. **UI Enhancements**
   - Show retrieval confidence scores
   - Highlight retrieved passages in original document
   - Multi-turn conversations with memory
   - Export chat history

5. **LLM Integration**
   - Add OpenAI, HuggingFace, or local Ollama LLMs
   - Fine-tune for your domain
   - Multi-language support

6. **Advanced Features**
   - Query expansion (rewrite questions)
   - Document summarization
   - Multi-document comparison
   - Citation tracking

---

## 🔌 Integrating an LLM (Optional)

The current app shows retrieved context. To add automatic answer generation:

### Option 1: OpenAI (Paid, Recommended)
```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are helpful. Answer using only the context provided."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
    ]
)
answer = response.choices[0].message.content
```

### Option 2: HuggingFace Hosted Inference (Free tier available)
```bash
pip install huggingface_hub
```

### Option 3: Local Ollama (Free)
```bash
# Install Ollama from ollama.ai
ollama pull mistral  # or any other model

# In Python:
from langchain_community.llms import Ollama
llm = Ollama(model="mistral")
answer = llm.invoke(prompt)
```

---

## 🎛️ Tools & Libraries Used

| Tool | Purpose | Version |
|------|---------|---------|
| **Streamlit** | Web UI | >=1.28.0 |
| **LangChain** | RAG orchestration | >=1.2.0 |
| **Chroma** | Vector database | >=1.5.0 |
| **Sentence-Transformers** | Embeddings | >=2.2.0 |
| **PyPDF** | PDF loading | >=6.0.0 |

---

## 📁 Project Structure

```
Assessment 1/
├── app_simple.py                          # ✨ Main Streamlit app (use this!)
├── Final_Copy_Mini_Project_4.ipynb        # Original notebook (reference)
├── rag_streamlit_app.py                   # Previous version (archived)
├── requirements.txt                       # Python dependencies
├── README.md                              # This file
├── apple_db/                              # Vector database (auto-created)
│   └── chroma.sqlite3
└── HBR_How_Apple_Is_Organized_For_Innovation-4.pdf  # Example PDF
```

---

## 🚀 Deployment

### Local Deployment (Development)
```bash
streamlit run app_simple.py
```

### Cloud Deployment

**Streamlit Cloud (Free)**
```bash
# Push to GitHub, then link at share.streamlit.io
```

**Heroku / AWS / Azure**
```bash
# Use requirements.txt for dependencies
# Ensure apple_db/ folder is initialized
```

**Docker Deployment**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app_simple.py"]
```

---

## ⚠️ Troubleshooting

### Issue: "Knowledge Base not found"
**Solution:** 
- Ensure PDF is in the project directory, OR
- Upload via Streamlit UI, OR
- Run the notebook first to create `apple_db/`

### Issue: Model download too slow
**Solution:**
- Pre-download: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('thenlper/gte-large')"`
- Use smaller model: `all-MiniLM-L6-v2`

### Issue: Out of memory
**Solution:**
- Reduce k_retrieve (fewer sources)
- Use smaller chunks
- Use GPU if available

---

## 📞 Support

- **Streamlit Docs:** https://docs.streamlit.io
- **LangChain Docs:** https://python.langchain.com
- **Chroma Docs:** https://docs.trychroma.com

---

## 📝 License

This project is provided as-is for educational purposes.

---

**Last Updated:** February 2026  
**Status:** ✅ Simplified & Production-Ready
