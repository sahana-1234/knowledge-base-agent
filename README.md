📘 Knowledge Base Agent (PDF-QA Chatbot using Chroma + Ollama + Streamlit)

A local, privacy-focused AI system that lets users:

✔ Upload multiple PDFs
✔ Ingest & embed them using ChromaDB
✔ Ask questions about the documents
✔ Chat with retrieved context
✔ Delete individual documents
✔ Toggle dark/light theme
✔ View processed document list

Built using: Ollama (Qwen 1.5B) + ChromaDB + Streamlit.

🚀 Features
🔍 1. Multi-document PDF Ingestion

Upload multiple PDFs

Automatic chunking

Embedding using nomic-embed-text

Stored locally in ChromaDB

🧠 2. Intelligent Retrieval + LLM Response

User question → Query vector DB → Retrieve best chunks

LLM (Ollama Qwen 1.5B) generates final answer

📄 3. Document Manager

List all uploaded documents

Show upload timestamp

Show number of chunks

Delete individual documents

🌗 4. Dark/Light Mode Toggle
💬 5. Persistent Chat History
🔐 6. Local Privacy

No cloud required — everything runs on your laptop.

🏗️ Tech Stack
Component	Technology
LLM	Ollama (Qwen 1.5B)
Embeddings	nomic-embed-text
Vector DB	ChromaDB
Backend	Python
UI	Streamlit
Tunneling	Ngrok
PDF Parsing	PyPDF2
📁 Project Structure
kb_agent/
├── app.py
├── ingest.py
├── chroma_client.py
├── data/
│   ├── sample_company_doc.pdf
│   ├── MAJOR-SYNOPSIS-Last1.pdf
├── db/                      # ChromaDB persistent storage
├── requirements.txt
└── chat_history.db

⚙️ Installation & Local Setup
1️⃣ Clone the repository
git clone https://github.com/sahana-1234/knowledge-base-agent.git
cd knowledge-base-agent

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install required Ollama models
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text

5️⃣ Run Streamlit app
streamlit run app.py

🌍 Optional: Public Demo Using Ngrok
cd C:\ngrok
./ngrok http --domain=yong-noninflationary-reactively.ngrok-free.dev 8501


Share the generated link:
👉 https://yong-noninflationary-reactively.ngrok-free.dev

🔮 Future Improvements

Fine-tuned model for your domain

Support for DOCX / Excel

Hybrid search (BM25 + embeddings)

Admin login panel

GPU inference support