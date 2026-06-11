import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import os

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
# Page Config
# =========================
st.set_page_config(
    page_title="AI Document Analyst",
    page_icon="📄",
    layout="wide"
)

# =========================
# Session State
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# =========================
# Header
# =========================
st.markdown(
    """
    <h1 style='text-align:center;color:#4CAF50;'>
        📄 AI Document Analyst
    </h1>

    <h4 style='text-align:center;'>
        Upload Any PDF and Ask Questions
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# =========================
# Sidebar
# =========================
st.sidebar.title("📌 AI Document Analyst")

st.sidebar.success("✅ PDF Question Answering")
st.sidebar.success("✅ Document Summary")
st.sidebar.success("✅ AI Analysis")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.history = []
    st.rerun()

# =========================
# Upload PDF
# =========================
uploaded_file = st.file_uploader(
    "📂 Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    st.session_state.pdf_text = text

    st.success("✅ PDF Uploaded Successfully")

# =========================
# Quick Actions
# =========================
st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    summary_btn = st.button("📄 Summary")

with col2:
    keypoints_btn = st.button("📌 Key Points")

with col3:
    report_btn = st.button("📊 Report")

# =========================
# Question Input
# =========================
query = st.text_input(
    "💬 Ask a Question"
)

# =========================
# Button Logic
# =========================
submit = False

if summary_btn:
    query = "Summarize this document"
    submit = True

elif keypoints_btn:
    query = "List key points from this document"
    submit = True

elif report_btn:
    query = "Generate a professional report"
    submit = True

elif st.button("🚀 Submit"):
    submit = True

# =========================
# Generate Answer
# =========================
if submit:

    if st.session_state.pdf_text == "":
        st.warning("Please upload a PDF first")

    elif query.strip() == "":
        st.warning("Please enter a question")

    else:

        with st.spinner("🤖 Analyzing Document..."):

            try:

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
You are an AI Document Analyst.

DOCUMENT:
{st.session_state.pdf_text[:1500]}

QUESTION:
{query}

Answer only from the document.

If information is not available,
reply:
Information not found in document.
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
                st.error(f"Error: {e}")

# =========================
# Chat History
# =========================
if st.session_state.history:

    st.subheader("💬 Chat History")

    for item in reversed(st.session_state.history):

        st.markdown(
            f"""
### 🙋 Question
{item['question']}

### 🤖 Answer
{item['answer']}
"""
        )

        st.markdown("---")

# =========================
# Footer
# =========================
st.markdown("---")

st.caption(
    "🚀 Built with Streamlit + Gemini AI"
)