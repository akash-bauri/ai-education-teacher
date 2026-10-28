
import traceback
from datetime import datetime

from chroma_manager import (
    get_context,
    get_source_information,
)

from utils import (
    search_web,
    format_web_results,
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
    """Build an educational prompt grounded in the supplied context."""

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
- Use the supplied reference content as the primary source.
- Do not invent facts from the document.
- If information is missing, state:
  "Information not available in the uploaded document."
- Explain concepts in simple, age-appropriate language.
- Focus on conceptual understanding rather than rote memorization.
- Include practical classroom examples and activities where relevant.
- Make the response useful and classroom-ready.

Use these sections when appropriate:

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

Explain what teachers and students should do for activities.
Describe expected learning outcomes.
Follow NCF 2023 and NEP 2020 principles.
Avoid irrelevant sections and unsupported claims.
"""


# ==========================================
# QUESTION ANSWERING
# ==========================================

def rag_answer(question, student_level="Class 5"):
    """
    Search uploaded documents first.
    Fall back to web search when document context is unavailable.
    """

    try:
        context = get_document_context(question)

        # Primary source: uploaded documents
        if context:
            prompt = build_education_prompt(
                question,
                context,
                student_level,
            )

            answer = call_llm(
                prompt,
                max_tokens=RAG_MAX_TOKENS,
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
                    "chunks_used": RAG_TOP_K,
                },
                "generated_at": get_timestamp(),
            }

        # Fallback source: web search
        web_results = search_web(question)

        if not web_results:
            return {
                "answer": (
                    "No relevant information was found in the "
                    "uploaded documents or web search. Try a more "
                    "specific question or upload a relevant document."
                ),
                "source": "No Source Found",
                "source_info": None,
                "generated_at": get_timestamp(),
            }

        web_context = format_web_results(web_results)

        if not web_context or not web_context.strip():
            return {
                "answer": "Web search returned no usable reference content.",
                "source": "Web Search",
                "source_info": None,
                "web_results": web_results,
                "generated_at": get_timestamp(),
            }

        prompt = build_education_prompt(
            question,
            web_context,
            student_level,
        )

        answer = call_llm(
            prompt,
            max_tokens=RAG_MAX_TOKENS,
        )

        return {
            "answer": answer,
            "source": "Web Search",
            "source_info": None,
            "web_results": web_results,
            "generated_at": get_timestamp(),
        }

    except Exception:
        traceback.print_exc()

        return {
            "answer": (
                "Sorry, I could not generate an answer right now. "
                "Please try again shortly. If the problem continues, "
                "check the Streamlit Cloud logs."
            ),
            "source": "Error",
            "source_info": None,
            "generated_at": get_timestamp(),
        }


# ==========================================
# NOTES GENERATOR
# ==========================================

def generate_document_notes(topic, student_level="Class 5"):
    """Generate study notes from uploaded document content."""

    try:
        context = get_document_context(topic)

        if not context:
            return (
                "No relevant content found in the uploaded document."
            )

        prompt = f"""
Generate NCF 2023 and NEP 2020 aligned study notes.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

REFERENCE DOCUMENT:
{context}

Include:
1. Chapter Overview
2. Learning Outcomes
3. Competencies
4. Key Concepts
5. Detailed Notes
6. Real-Life Examples
7. Activity-Based Learning
8. Inclusive Teaching Strategies
9. Flow Chart
10. Mind Map
11. Revision Notes
12. Summary

Use simple, age-appropriate language.
Prioritize information in the reference document.
Do not invent document-specific facts.
If a fact is unavailable, clearly identify the limitation.
Keep the notes organized and useful for revision.
"""

        return call_llm(
            prompt,
            max_tokens=NOTES_MAX_TOKENS,
        )

    except Exception:
        traceback.print_exc()
        return "Could not generate notes. Please check the application logs."


# ==========================================
# MCQ GENERATOR
# ==========================================

def generate_document_mcqs(topic, difficulty="Mixed"):
    """Generate document-grounded, competency-based MCQs."""

    try:
        context = get_document_context(topic)

        if not context:
            return (
                "No relevant content found in the uploaded document."
            )

        prompt = f"""
Generate competency-based MCQs aligned with NCF 2023 principles.

TOPIC:
{topic}

REFERENCE DOCUMENT:
{context}

DIFFICULTY:
{difficulty}

Create a concise set of questions covering the requested topic.
When appropriate, include a mix of:
- Single Correct Answer
- Multiple Correct Answers
- All of the Above
- None of the Above
- Assertion and Reason
- Case-Based Questions
- Application-Based Questions
- Critical Thinking
- Real-Life Scenarios
- Activity-Based Questions

Organize questions under:
# Learning Outcomes
# Competencies
# Easy Questions
# Moderate Questions
# Hard Questions

For each question provide:
Question Type
Question
Options A, B, C, D
Correct Answer
Brief Explanation
Competency Assessed
Learning Outcome Assessed

Use clear, unambiguous options.
For multiple-answer questions, identify every correct option.
Ensure the answer key matches the options.
Use the reference document as the primary source.
Do not invent facts unsupported by the document.
Keep the output concise and educationally useful.
"""

        return call_llm(
            prompt,
            max_tokens=MCQ_MAX_TOKENS,
        )

    except Exception:
        traceback.print_exc()
        return "Could not generate MCQs. Please check the application logs."


# ==========================================
# QUESTION PAPER GENERATOR
# ==========================================

def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed",
):
    """Generate a question paper based on uploaded document content."""

    try:
        context = get_document_context(topic)

        if not context:
            return (
                "No relevant content found in the uploaded document."
            )

        prompt = f"""
Generate a question paper aligned with NCF 2023 principles.

TOPIC:
{topic}

REFERENCE DOCUMENT:
{context}

TOTAL MARKS:
{marks}

DIFFICULTY:
{difficulty}

Prepare a paper appropriate to the requested topic and level.

Include:
# Learning Outcomes
# Competencies
# Instructions
# Marks Distribution

## Section A: Easy Questions
## Section B: Moderate Questions
## Section C: Hard Questions
## Section D: Case-Based Questions
## Section E: Activity-Based Questions

Finish with:
# Answer Key
# Competency Mapping

Rules:
- The total marks must equal {marks}.
- Show the marks for every question.
- Keep questions relevant to the topic and reference document.
- Focus on conceptual understanding and real-life application.
- Use age-appropriate language.
- Do not invent facts unsupported by the document.
- Keep the paper concise enough to fit the response limit.
"""

        return call_llm(
            prompt,
            max_tokens=QUESTION_PAPER_MAX_TOKENS,
        )

    except Exception:
        traceback.print_exc()
        return (
            "Could not generate the question paper. "
            "Please check the application logs."
        )
