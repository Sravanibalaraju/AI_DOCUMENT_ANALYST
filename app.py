import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pypdf import PdfReader

# =========================
# Load API Key
# =========================
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key not found")
    st.stop()

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

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.history = []
    st.rerun()

st.sidebar.success("✅ Gemini Connected")

# =========================
# Upload PDF
# =========================
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file is not None:

    try:
        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text

        st.success("✅ PDF Uploaded Successfully")

    except Exception as e:
        st.error(f"Error Reading PDF: {e}")

# =========================
# Quick Buttons
# =========================
st.subheader("⚡ Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("📄 Summary"):
        st.session_state["query"] = "Summarize this document"

with c2:
    if st.button("📊 Key Points"):
        st.session_state["query"] = "List key points"

with c3:
    if st.button("📋 Report"):
        st.session_state["query"] = "Generate a professional report"

# =========================
# Question Input
# =========================
query = st.text_input(
    "Ask a Question",
    value=st.session_state.get("query", "")
)

# =========================
# Submit Button
# =========================
submit = st.button("🚀 Submit")

# =========================
# Generate Answer
# =========================
if submit:

    if uploaded_file is None:
        st.warning("Please upload a PDF first")

    elif query.strip() == "":
        st.warning("Please enter a question")

    else:

        with st.spinner("🤖 Generating Answer..."):

            try:

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
You are an intelligent PDF assistant.

Answer ONLY using the document content below.

If the answer is not available in the document,
say:
Information not found in document.

DOCUMENT:
{pdf_text[:5000]}

QUESTION:
{query}
"""

                response = model.generate_content(prompt)

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