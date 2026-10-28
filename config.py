# config.py
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default=None):
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key, default)

# =====================================================
# 🔐 EXISTING ENVIRONMENT CONFIGURATIONS
# =====================================================
GROQ_API_KEY = get_env("GROQ_API_KEY")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")

# =====================================================
# 📊 NEW CENTRALIZED VERSION 1.0 MVP STRINGS & CONTEXTS
# =====================================================
APP_VERSION = "Version 1.0 MVP"
EMBEDDING_MODEL = "all-MiniLM-L6-v2 (384D)"
LLM_MODEL = "Llama-3.3-Groq Engine"
VECTOR_DATABASE = "FAISS (FlatL2 Memory Local)"

# Validation Rules
MAX_FILE_SIZE_MB = 15
MIN_WORD_COUNT = 15

# Core UI Actions
DOCUMENT_DEPENDENT_ACTIONS = [
    "📦 Generate Complete Teaching Package",
    "Generate Notes",
    "Generate MCQs",
    "Generate Question Paper",
    "Generate Learning Outcomes",
    "Generate Competencies",
    "Generate Lesson Plan",
    "Generate Teaching Guide",
    "Generate Flow Chart",
    "Generate Mind Map",
    "Generate Chapter Summary",
    "Generate Important Questions"
]
