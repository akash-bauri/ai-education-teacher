
import traceback
from datetime import datetime

from chroma_manager import (
    get_context,
    get_source_information
)

from utils import (
    search_web,
    format_web_results
)

from llm_service import call_llm


# ==========================================
# CONFIGURATION
# ==========================================

RAG_TOP_K = 5
RAG_MAX_TOKENS = 800
NOTES_MAX_TOKENS = 800
MCQ_MAX_TOKENS = 800
QUESTION_PAPER_MAX_TOKENS = 800


# ==========================================
# COMMON HELPERS
# ==========================================

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_document_context(query, top_k=RAG_TOP_K):
    """Retrieve relevant context from the document knowledge base."""
    context = get_context(query, top_k=top_k)

    if not context:
        return ""

    return context.strip()


def build_education_prompt(topic, context, student_level):
    """Build a source-grounded, NCF 2023 and NEP 2020 aligned prompt."""

    return f"""
You are an expert AI Teacher Assistant aligned with NCF 2023
and NEP 2020.

TOPIC OR QUESTION:
{topic}

STUDENT LEVEL:
{student_level}

REFERENCE CONTENT:
{context}

INSTRUCTIONS:
- Use the reference content as your primary source.
- Do not invent document-specific facts.
- If the reference does not contain the requested information,
  clearly say: "Information not available in the uploaded document."
- Explain concepts in simple, age-appropriate language.
- Focus on conceptual understanding, not rote memorization.
- Include practical classroom examples and activities where relevant.
- Keep the response useful, organized, and classroom-ready.

Use the following structure when appropriate:

# Simple Explanation
# Learning Outcomes
# Competencies
# Key Concepts
# Real-Life Examples
# Activity-Based Learning
# Inclusive Teaching Strategies
# Flow Chart
# Mind Map
# Assessment Questions
## Easy Questions
## Moderate Questions
## Hard Questions
# Exam Tips
# Summary

For each activity, explain what the teacher and students should do
and describe the expected learning outcome.

Do not force irrelevant sections into answers where they are
not suitable. Align educational suggestions with NCF 2023
and NEP 2020.
"""


# ==========================================
# QUESTION ANSWERING
# ==========================================

def rag_answer(question, student_level="Class 5"):
    """
    Answer using the document knowledge base first.
    Use web search only when document context is unavailable.
    """

    try:
        context = get_document_context(question)

        # ----------------------------------
        # PRIMARY SOURCE: DOCUMENT KNOWLEDGE
        # ----------------------------------
        if context:
            prompt = build_education_prompt(
                question,
                context,
                student_level
            )

            answer = call_llm(
                prompt,
                max_tokens=RAG_MAX_TOKENS
            )

            try:
                source_info = get_source_information(question)
            except Exception:
                source_info = None

            return {
                "answer": answer,
                "source": "Document Knowledge Base",
                "source_info": source_info,
                "retrieval": {
                    "method": "Semantic Search",
                    "chunks_used": RAG_TOP_K
                },
                "generated_at": get_timestamp()
            }

        # ----------------------------------
        # FALLBACK SOURCE: WEB SEARCH
        # ----------------------------------
        web_results = search_web(question)

        if not web_results:
            return {
                "answer": (
                    "No relevant information was found in the "
                    "uploaded documents or web search. Please try "
                    "a more specific question or upload a relevant document."
                ),
                "source": "No Source Found",
                "source_info": None,
                "generated_at": get_timestamp()
            }

        web_context = format_web_results(web_results)

        if not web_context or not web_context.strip():
            return {
                "answer": (
                    "Web search returned no usable reference content. "
                    "Please try again or rephrase your question."
                ),
                "source": "Web Search",
                "source_info": None,
                "web_results": web_results,
                "generated_at": get_timestamp()
            }

        prompt = build_
