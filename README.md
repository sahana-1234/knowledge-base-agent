📘 Knowledge Base Agent (PDF-QA Chatbot using Chroma + Ollama + Streamlit)
🧩 Overview

The Knowledge Base Agent is an AI-powered system that allows users to upload PDF documents and interact with them through a conversational chat interface.
It uses local LLM inference through Ollama, combined with ChromaDB vector search, to answer user queries strictly based on uploaded documents.
This ensures privacy, accuracy, and offline capability.
-------------------------------------------------------------------------
🚀 Features
🔍 1. Multi-document PDF Ingestion

Upload multiple PDFs

Automatic text extraction

Text chunking using RecursiveCharacterTextSplitter

Embedding generated using nomic-embed-text

Stored locally in ChromaDB

🧠 2. Retrieval-Augmented Generation (RAG)

User question → semantic search in vector DB → best chunks retrieved

LLM (Ollama Qwen 1.5B) generates answer ONLY from documents

Prevents hallucination using a strict prompt template

📄 3. Document Manager

List all uploaded documents

Display file name, upload timestamp, number of chunks

Delete individual documents from vector DB

🌗 4. Dark/Light Mode Toggle

Clean UI with modern theme and automatic text color updates.

💬 5. Persistent Chat History

Conversation stays on screen until the user clears it.

🔐 6. Fully Local & Private

No cloud calls

All embeddings + inference happen on the user's machine

Perfect for confidential data
--------------------------------------------------------------------------------------------
⚠️ Limitations

Even though the agent is powerful, it has some limitations:

❌ Requires laptop to be ON for Ngrok demo link

❌ Slow on low-performance CPUs (LLM runs locally)

❌ Cannot answer questions outside uploaded documents

❌ Limited model size (Qwen 1.5B is small compared to GPT-4)

❌ No online LLM API support

❌ No user authentication (anyone with link can use it)
--------------------------------------------------------------------------------------------
🏗️ Tech Stack

| Component                | Technology              |
| ------------------------ | ----------------------- |
| **Local LLM**            | Ollama — *Qwen2.5:1.5B* |
| **Embeddings**           | nomic-embed-text        |
| **Vector Database**      | ChromaDB                |
| **Frontend UI**          | Streamlit               |
| **Frameworks**           | LangChain, PyPDFLoader  |
| **Deployment (Demo)**    | Ngrok                   |
| **Programming Language** | Python                  |

-------------------------------------------------------------------------------------
🧱 Architecture Diagram (High-Level)

            ┌──────────────────────────┐
            │        User UI           │
            │     (Streamlit App)      │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │ PDF Upload & Processing  │
            │  (PyPDFLoader, Splitter) │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │  Embedding Generation    │
            │  (Ollama Embeddings)     │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │   ChromaDB Vector Store  │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │    Retriever (k=5)       │
            └────────────┬─────────────┘
                         │
                         ▼
            ┌──────────────────────────┐
            │    Ollama LLM (Qwen)     │
            │  Generate Final Answer   │
            └──────────────────────────┘
----------------------------------------------------------------------------------
📁 Project Structure

kb_agent/
├── app.py
├── ingest.py
├── chroma_client.py
├── data/
│   ├── sample_company_doc.pdf
│   ├── MAJOR-SYNOPSIS-Last1.pdf
├── db/
├── requirements.txt
└── chat_history.db

-----------------------------------------------------------------------------------
⚙️ Installation & Local Setup
1️⃣ Clone the repository
git clone https://github.com/sahana-1234/knowledge-base-agent.git
cd knowledge-base-agent

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install required Ollama models
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text

5️⃣ Run the Streamlit app
streamlit run app.py
---------------------------------------------------------------------------
🌍 Public Demo (Ngrok - Required for Jury)

Start Streamlit:

streamlit run app.py


Start Ngrok with permanent domain:

cd C:\ngrok
./ngrok http --domain=yong-noninflationary-reactively.ngrok-free.dev 8501
------------------------------------------------------------------

Your demo link:

👉 https://yong-noninflationary-reactively.ngrok-free.dev
---------------------------------------------------------------------------

🔮 Future Improvements

Larger LLM support (LLaMA, Mixtral, Phi-3)

Cloud deployment using API-based LLMs

OCR support for scanned PDFs

User authentication

Multi-user document isolation

DOCX, PPTX, XLSX support

GPU acceleration

Faster retrieval using hybrid search

Document summary mode
