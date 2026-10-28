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
# COMMON DOCUMENT CHECK
# ==========================================

def get_document_context(
    query,
    top_k=5
):
    """
    Retrieve context from ChromaDB.
    """
    context = get_context(
        query,
        top_k=top_k
    )
    return context.strip()


# ==========================================
# EDUCATION PROMPT BUILDER
# ==========================================

def build_education_prompt(
    topic,
    context,
    student_level
):
    return f"""
Create a complete NCF 2023 aligned explanation.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

REFERENCE CONTENT:
{context}

Generate:

# Simple Explanation

Explain like a teacher.

# Learning Outcomes

# Competencies

# Key Concepts

# Real Life Examples

# Activity Based Learning

# Inclusive Teaching Strategy

# Flow Chart

Use arrows.

# Mind Map

Use tree structure.

# Assessment Questions

Easy Questions

Moderate Questions

Hard Questions

# Exam Tips

# Summary

Use simple language.

Focus on conceptual understanding.

IMPORTANT INSTRUCTIONS
Use the uploaded document as the PRIMARY source.
Never invent facts that are not present inside the retrieved document.
If information is missing from the uploaded document, clearly state:
"Information not available in the uploaded document."
Prefer conceptual understanding.
Generate classroom-ready explanations.
Follow NCF 2023 and NEP 2020.
Avoid hallucinations.
Always explain like an experienced teacher.
"""


# ==========================================
# QUESTION ANSWERING
# ==========================================

def rag_answer(
    question,
    student_level="Class 5"
):
    try:
        # -----------------------------
        # ChromaDB Search
        # -----------------------------
        context = get_document_context(
            question
        )

        if context:
            prompt = build_education_prompt(
                question,
                context,
                student_level
            )

            answer = call_llm(
                prompt,
                max_tokens=2500
            )

            # Extract rich enterprise metadata for traceability
            source_info = get_source_information(
                question
            )

            return {
                "answer": answer,
                "source": "Document Knowledge Base",
                "source_info": source_info,
                "retrieval": {
                    "method": "FAISS Semantic Search",
                    "chunks_used": 5
                },
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        # -----------------------------
        # Web Search Fallback
        # -----------------------------
        web_results = search_web(
            question
        )

        web_context = format_web_results(
            web_results
        )

        prompt = build_education_prompt(
            question,
            web_context,
            student_level
        )

        answer = call_llm(
            prompt,
            max_tokens=2500
        )

        return {
            "answer": answer,
            "source": "Web Search",
            "source_info": None,
            "web_results": web_results,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception:
        return {
            "answer": traceback.format_exc(),
            "source": "Error",
            "source_info": None,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# ==========================================
# NOTES GENERATOR
# ==========================================

def generate_document_notes(
    topic,
    student_level="Class 5"
):
    context = get_document_context(
        topic
    )

    if not context:
        return (
            "No relevant content found "
            "in uploaded document."
        )

    prompt = f"""
Generate NCF 2023 aligned study notes.

TOPIC:
{topic}

DOCUMENT:
{context}

STUDENT LEVEL:
{student_level}

Generate:

# Chapter Overview

# Learning Outcomes

# Competencies

# Key Concepts

# Detailed Notes

# Real Life Examples

# Activity Based Learning

# Inclusive Teaching Strategy

# Flow Chart

# Mind Map

# Revision Notes

# Summary

Explain as a teacher.
"""

    return call_llm(
        prompt,
        max_tokens=2200
    )


# ==========================================
# MCQ GENERATOR (UPDATED PROMPT)
# ==========================================

def generate_document_mcqs(
    topic,
    difficulty="Mixed"
):
    context = get_document_context(
        topic
    )

    if not context:
        return (
            "No relevant content found "
            "in uploaded document."
        )

    prompt = f"""
Generate NCF 2023 aligned competency-based MCQs.

TOPIC:
{topic}

DOCUMENT:
{context}

DIFFICULTY:
{difficulty}

IMPORTANT:

Generate a balanced mix of question types.

Question Distribution:

1. Single Correct Answer MCQs
   - Only one option is correct.

2. Multiple Correct Answer MCQs
   - Two or more options are correct.

3. All of the Above Questions
   - All options are correct.

4. None of the Above Questions
   - None of the options are correct.

5. Assertion and Reason Questions

6. Case Based MCQs

7. Application Based MCQs

8. Critical Thinking MCQs

9. Real Life Scenario MCQs

10. Activity Based MCQs

Generate:

# Learning Outcomes

# Competencies

# Easy Level MCQs (5)

# Moderate Level MCQs (5)

# Hard Level MCQs (5)

For every question provide:

Question Type:
(Single Correct / Multiple Correct / All of the Above /
None of the Above / Case Based /
Assertion Reason / Activity Based)

Question:

A.
B.
C.
D.

Correct Answer:

Explanation:

Competency Assessed:

Learning Outcome Assessed:

IMPORTANT RULES:

- Randomly mix all question types.
- Do not make all questions single-correct.
- At least 20% should be Multiple Correct.
- At least 10% should be All of the Above.
- At least 10% should be None of the Above.
- Include competency-based assessment.
- Include real-life examples.
- Include case-based questions.
- Include application-based questions.
- Include activity-based questions.
- Follow NCF 2023 guidelines.
- Avoid rote memorization.
- Focus on conceptual understanding and application.
"""

    return call_llm(
        prompt,
        max_tokens=2500
    )


# ==========================================
# QUESTION PAPER GENERATOR
# ==========================================

def generate_document_question_paper(
    topic,
    marks=20,
    difficulty="Mixed"
):
    context = get_document_context(
        topic
    )

    if not context:
        return (
            "No relevant content found "
            "in uploaded document."
        )

    prompt = f"""
Generate a complete NCF 2023 aligned question paper.

TOPIC:
{topic}

DOCUMENT:
{context}

TOTAL MARKS:
{marks}

DIFFICULTY:
{difficulty}

Generate:

# Learning Outcomes

# Competencies

SECTION A
Easy Questions

SECTION B
Moderate Questions

SECTION C
Hard Questions

SECTION D
Case Based Questions

SECTION E
Activity Based Questions

Provide:

- Marks Distribution
- Answer Key
- Competency Mapping

Focus on conceptual understanding.
"""

    return call_llm(
        prompt,
        max_tokens=3500
    )
