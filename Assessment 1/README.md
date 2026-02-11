# RAG (Retrieval-Augmented Generation) Question Answering System

## 📋 Project Overview

This is a production-ready Retrieval-Augmented Generation (RAG) system built with **Streamlit**, **LangChain**, **Chroma**, and **Sentence-Transformers**. It allows you to upload PDF documents and ask natural language questions that are answered using semantic search combined with optional local LLM generation.

**Key Features:**
- 🚀 Interactive Streamlit web interface with chat history
- 🔍 Semantic search with Chroma vector database
- 🧠 Sentence-Transformer embeddings (gte-large model)
- 💾 Persistent vector database (SQLite-backed)
- 📱 Beautiful chat interface with message history
- 🎛️ Configurable retrieval settings (k, max tokens, models)
- 🤖 **Dual LLM Options**: Ollama (SmolLM/Mistral) or Context-only fallback
- 📄 PDF document upload and indexing

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

## 📊 RAG Pipeline Architecture

```
┌─────────────────────────────────────────┐
│           RAG PIPELINE FLOW              │
└─────────────────────────────────────────┘

    ┌──────────────────┐
    │  User Question   │  (Natural language input)
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  Query Embedding             │  (gte-large / mini)
    │  Convert Q to 1024-dim vector│
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  Vector Store Search         │  (Chroma / FAISS)
    │  Retrieve top-k chunks       │  (Similarity or MMR)
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  Retrieved Context           │  (Top-k document chunks)
    │  Build prompt with context   │  (512 chars chunks, 20 overlap)
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  LLM Generation (Optional)   │  (Ollama: SmolLM or Mistral)
    │  OR Context Display          │  (Fallback: show chunks)
    └────────┬─────────────────────┘
             │
             ▼
    ┌──────────────────────────────┐
    │  User Gets Accurate Answer   │  (Grounded in documents)
    │  Sources visible in UI       │  (Traceable & transparent)
    └──────────────────────────────┘
```

**Key Features of This Architecture:**
- **Semantic Search:** Uses embeddings to find relevant context
- **Chunking Strategy:** 512 chars with 20-char overlap
- **Dual LLM Options:** SmolLM (fast) or Mistral (quality)
- **Fallback Mechanism:** Shows context if LLM unavailable
- **Grounded Answers:** No hallucinations (answers from documents)

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

## 🤖 LLM Options - Dual Choice Architecture

This project implements **2 configurable LLM choices**:

### **Choice 1: Ollama (Local, Free, Recommended)**
Deploy locally without external API keys. Two model options:

#### SmolLM (Lightweight)
- **Best For:** Low RAM systems (<4GB), fast response
- **Speed:** Very fast (~50-100 tokens/sec)
- **Quality:** Good for simple Q&A
- **Setup:**
```bash
# Install Ollama from ollama.ai
ollama pull smollm

# Configure in app (Streamlit sidebar)
Model dropdown → Select "smollm"
```

#### Mistral 7B (High Quality)
- **Best For:** High-quality answers, detailed responses
- **Speed:** Slower (~20-50 tokens/sec)
- **Quality:** Excellent, production-ready
- **Requirements:** ~4.5GB RAM + 7GB disk
- **Setup:**
```bash
ollama pull mistral
# Configure in app
Model dropdown → Select "mistral"
```

### **Choice 2: Fallback (Context Display)**
If Ollama is not available or disabled:
- Shows retrieved document chunks directly
- Still provides accurate information (grounded retrieval)
- No hallucinations or errors
- Good for read-only use cases

### Implementation in App
```python
# From rag_streamlit_app.py
use_llm = st.checkbox("Use local LLM (Ollama)", value=True)
ollama_model = st.selectbox("Model", ["smollm", "mistral"], index=0)

if use_ollama and context.strip():
    answer = generate_answer_ollama(context, query, model=ollama_model)
else:
    answer = context  # Fallback: show context directly
```

---

## 📖 Instructions to Run the Notebook

### Prerequisites
- Python 3.8+
- 4GB+ RAM (8GB+ for Mistral)
- Ollama installed (optional, for LLM features)

### Step-by-Step Guide

#### **Step 1: Install Dependencies**
```bash
# Navigate to project directory
cd "k:\GitHub\Agentic-AI\Assessment 1"

# Create virtual environment
python -m venv venv

# Activate venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements.txt
```

#### **Step 2: Prepare PDF (Optional)**
- Place PDF in project directory, OR
- Use default: `HBR_How_Apple_Is_Organized_For_Innovation-4.pdf`
- Or upload via Streamlit UI

#### **Step 3: Install Ollama (Optional, for LLM answers)**
```bash
# Download from ollama.ai
# Then pull a model:
ollama pull smollm    # or: ollama pull mistral
```

#### **Step 4: Run Streamlit App**
```bash
streamlit run rag_streamlit_app.py
```
The app opens at `http://localhost:8501`

#### **Step 5: Use the App**
1. **Upload PDF** (sidebar) or use default
2. **Ask a question** in chat input
3. **Select settings** (sidebar):
   - "Sources to retrieve" (k): 1-5
   - "Max answer length": 64-256 tokens
   - "Use local LLM": toggle for Ollama
   - "Model": choose smollm or mistral
4. **View results**:
   - Answer (from Ollama or context)
   - Sources (expand to see chunks)

### Running the Jupyter Notebook

If you prefer notebook format:
```bash
# Install Jupyter
pip install jupyter

# Start notebook
jupyter notebook Rag.ipynb
```

Then run cells in order:
1. Import libraries
2. Load PDF
3. Build embeddings & vector store
4. Test retrieval
5. Generate answers

## 🎛️ Tools & Libraries Used

| Tool | Purpose | Version | Notes |
|------|---------|---------|-------|
| **Streamlit** | Web UI Framework | >=1.28.0 | Interactive chat interface & visualization |
| **LangChain** | RAG Orchestration | >=0.2.0 | Manages retrieval + generation pipeline |
| **LangChain-Community** | Extended Integrations | >=0.2.0 | PDF loading, embeddings, vector stores |
| **Chroma** | Vector Database | >=0.4.0 | Persistent SQLite-backed vector store |
| **Sentence-Transformers** | Embedding Model | >=2.2.0 | gte-large (1024-dim, 500MB download) |
| **PyPDF** | PDF Document Loading | >=3.0.0 | Extracts text from PDF pages |
| **LangChain-Text-Splitters** | Text Chunking | >=0.2.0 | Recursive character splitter (512 chars, 20 overlap) |
| **Ollama** (Optional) | Local LLM Runtime | Latest | SmolLM (lightweight) or Mistral (high quality) |

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
## 🌐 Live Demo

**Try the live application here:**  
🔗 [RAG System - Live Streamlit App](https://agentic-ai-wi3a4vkowughecg7verxkc.streamlit.app/)

---

## 📝 License

This project is provided as-is for educational purposes.

---

