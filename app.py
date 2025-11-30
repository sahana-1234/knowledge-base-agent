import os
import streamlit as st
import tempfile
from datetime import datetime
from chroma_client import client
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------------------------------------------------
# 🌈 PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Knowledge Base Agent", page_icon="📘", layout="wide")

# ---------------------------------------------------------
# 🌙 DARK MODE TOGGLE
# ---------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark

if dark:
    BG = "#0e1117"
    BG_GRAD = "linear-gradient(to bottom, #0e1117, #161b22)"
    USER = "#1f6feb"
    BOT = "#21262d"
    TEXT = "white"
else:
    BG = "#f5f7fa"
    BG_GRAD = "linear-gradient(to bottom, #eef2f3, #ffffff)"
    USER = "#d1e7ff"
    BOT = "#f8d7da"
    TEXT = "black"
st.markdown(f"""
<style>

/* GLOBAL TEXT FIX — ALL TITLES, LABELS, HEADERS MUST BE WHITE IN DARK MODE */
html, body, [data-testid="stAppViewContainer"], 
h1, h2, h3, h4, h5, h6,
p, label, span, div, strong {{
    color: {TEXT} !important;
}}

/* Fix for Streamlit-generated headers (title, subheader spacing blocks) */
span[data-testid="stHeader"], 
div[data-testid="stHeader"] *,
h1[class*="st"] *,
h2[class*="st"] *,
h3[class*="st"] *,
h4[class*="st"] *,
h5[class*="st"] *,
h6[class*="st"] * {{
    color: {TEXT} !important;
}}

/* Fix: File uploader label text */
[data-testid="stFileUploader"] label *,
[data-testid="stFileUploader"] div *,
[data-testid="stFileUploader"] span * {{
    color: {TEXT} !important;
}}

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {{
    background: {BG_GRAD};
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background: rgba(255,255,255,0.05);
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

/* CHAT BUBBLES */
.chat-bubble {{
    padding: 14px 20px;
    margin: 12px 0;
    border-radius: 18px;
    max-width: 80%;
    line-height: 1.5;
    font-size: 16px;
}}

.user {{
    background: rgba(91,123,255,0.25);
    margin-left: auto;
}}

.bot {{
    background: rgba(255,95,95,0.18);
}}

</style>
""", unsafe_allow_html=True)


st.title("📘 Knowledge Base Agent (Ollama)")

# ---------------------------------------------------------
# 🧠 VECTOR DB (Chroma 0.5+)
# ---------------------------------------------------------
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen2.5:1.5b"
embeddings = OllamaEmbeddings(model=EMBED_MODEL)

vector_db = Chroma(
    client=client,
    collection_name="kb_agent",
    embedding_function=embeddings,
)

retriever = vector_db.as_retriever(search_kwargs={"k": 5})
llm = ChatOllama(model=LLM_MODEL, temperature=0.2)

# ---------------------------------------------------------
# 📥 STORAGE FOR DOCUMENT METADATA
# ---------------------------------------------------------
if "doc_metadata" not in st.session_state:
    st.session_state.doc_metadata = {}  # {filename: {"uploaded_at": ts, "chunks": int}}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# ---------------------------------------------------------
# 📤 PDF INGESTION
# ---------------------------------------------------------
def ingest_uploaded_pdf(uploaded_file):
    tmp = tempfile.mkdtemp()
    pdf_path = os.path.join(tmp, uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    docs = PyPDFLoader(pdf_path).load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # Add metadata for tracking and deletion
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for chunk in chunks:
        chunk.metadata = {
            "source": uploaded_file.name,
            "uploaded_at": timestamp,
        }

    vector_db.add_documents(chunks)

    # Save metadata to session
    st.session_state.doc_metadata[uploaded_file.name] = {
        "uploaded_at": timestamp,
        "chunks": len(chunks),
    }

# ---------------------------------------------------------
# 🗂 SIDEBAR DOCUMENT LIST + DELETE
# ---------------------------------------------------------
st.sidebar.subheader("📄 Uploaded Documents")

if len(st.session_state.doc_metadata) == 0:
    st.sidebar.info("No documents uploaded yet.")
else:
    for filename, info in st.session_state.doc_metadata.items():
        st.sidebar.write(f"""
        **📄 {filename}**  
        ⏱ Uploaded: {info['uploaded_at']}  
       
        """)

        if st.sidebar.button(f"🗑 Delete {filename}", key=f"del_{filename}"):

            # Delete only this document's chunks
            vector_db.delete(where={"source": filename})

            # Remove metadata
            st.session_state.processed_files.discard(filename)
            del st.session_state.doc_metadata[filename]

            st.sidebar.success(f"Deleted {filename}")
            st.rerun()

# ---------------------------------------------------------
# 📤 FILE UPLOADER
# ---------------------------------------------------------
st.subheader("📤 Upload PDF Document")

uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf:
    if uploaded_pdf.name not in st.session_state.processed_files:
        with st.spinner(f"Processing {uploaded_pdf.name}..."):
            ingest_uploaded_pdf(uploaded_pdf)

        st.session_state.processed_files.add(uploaded_pdf.name)
        st.success(f"{uploaded_pdf.name} added successfully!")
    else:
        st.info(f"{uploaded_pdf.name} already processed.")

# ---------------------------------------------------------
# 💬 CHAT SYSTEM
# ---------------------------------------------------------
def retrieve_documents(retriever, query):
    methods = [
        "get_relevant_documents",
        "retrieve",
        "get_relevant_docs",
        "get_documents",
        "retrieve_documents",
        "invoke",
        "get_docs",
    ]
    for m in methods:
        if hasattr(retriever, m):
            try:
                docs = getattr(retriever, m)(query)
                return list(docs) if docs else []
            except:
                continue
    try:
        return list(retriever(query))
    except:
        return []

if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat history
for role, text in st.session_state.chat:
    bubble = "user" if role == "user" else "bot"
    st.markdown(f"<div class='chat-bubble {bubble}'>{text}</div>", unsafe_allow_html=True)

query = st.chat_input("Ask your question...")

if query:
    st.session_state.chat.append(("user", query))

    docs = retrieve_documents(retriever, query)

    context = "\n\n".join(
        d.page_content if hasattr(d, "page_content") else str(d)
        for d in docs
    )

    prompt = f"""
Use ONLY the context below.

If the answer is not present, reply:
"I don't know based on the documents."

Context:
{context}

Question: {query}
Answer:
"""

    result = llm.invoke(prompt).content
    answer = f"<br>{result.replace(chr(10), '<br>')}"

    st.session_state.chat.append(("assistant", answer))
    st.rerun()
