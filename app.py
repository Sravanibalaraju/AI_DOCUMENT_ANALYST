import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pypdf import PdfReader

# =========================
# Load Environment Variables
# =========================
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# =========================
# Streamlit Config
# =========================
st.set_page_config(
    page_title="AI Document Analyst",
    layout="wide"
)

# =========================
# Session State
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# Header
# =========================
st.title("📄 AI Document Analyst")
st.write("Upload any PDF and ask questions")

# =========================
# Sidebar
# =========================
st.sidebar.title("📄 AI Document Analyst")
st.sidebar.success("✅ Gemini Connected")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# =========================
# PDF Upload
# =========================
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:

    try:

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        st.success("✅ PDF Uploaded Successfully")

    except Exception as e:
        st.error(f"PDF Error: {e}")

# =========================
# Question Input
# =========================
query = st.text_input(
    "Ask a Question"
)

# =========================
# Buttons
# =========================
col1, col2 = st.columns(2)

with col1:
    submit = st.button("🚀 Submit")

with col2:
    clear = st.button("🗑 Clear Chat")

if clear:
    st.session_state.history = []
    st.rerun()

# =========================
# Gemini Response
# =========================
if submit:

    if uploaded_file is None:
        st.warning("Please upload a PDF first")

    elif query.strip() == "":
        st.warning("Please enter a question")

    else:

        with st.spinner("Generating Answer..."):

            try:

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
You are an intelligent PDF assistant.

Answer ONLY using the document content below.

If the answer is not available in the document,
say:
'Information not found in document.'

DOCUMENT:
{pdf_text[:20000]}

QUESTION:
{query}
"""

                response = model.generate_content(
                    prompt
                )

                answer = response.text

                st.session_state.history.append(
                    {
                        "question": query,
                        "answer": answer
                    }
                )

            except Exception as e:

                st.error(str(e))

# =========================
# Chat History
# =========================
if st.session_state.history:

    st.subheader("💬 Chat History")

    for item in reversed(st.session_state.history):

        st.markdown(
            f"### 🙋 Question\n{item['question']}"
        )

        st.markdown(
            f"### 🤖 Answer\n{item['answer']}"
        )

        st.markdown("---")