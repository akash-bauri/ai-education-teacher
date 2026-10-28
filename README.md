RAG-Based Generative AI Application for Educators

An AI-powered educational assistant that transforms uploaded PDF, DOCX, and TXT documents into classroom-ready teaching resources using Retrieval-Augmented Generation (RAG), semantic search, sentence-transformer embeddings, FAISS vector search, and a Large Language Model served through Groq.

The application is designed around NCF 2023 and NEP 2020 teaching principles and provides configurable resources for teachers and learners, including notes, MCQs, question papers, lesson plans, teaching guides, mind maps, flow charts, summaries, and important questions.

Version: 1.0 MVP
Deployment: Streamlit
Primary use case: Document-grounded educational content generation

🎯 Why This Project?

Teachers often spend significant time converting reference material into lesson plans, assessments, explanations, activities, and revision material.

This project demonstrates how a document-grounded Generative AI pipeline can reduce that preparation effort while keeping generated content connected to the user's uploaded source material.

The key engineering objective is not simply to call an LLM, but to build a pipeline that:

Accepts educational documents.

Extracts and prepares the source text.

Splits the source into searchable chunks.

Converts chunks into semantic embeddings.

Builds a FAISS vector index.

Retrieves the most relevant chunks for a query.

Passes retrieved context to the LLM.

Generates structured, classroom-ready resources.

Exposes retrieval and source metadata for transparency.

🏗️ System Architecture

                    ┌─────────────────────┐
                    │     Streamlit UI     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Document Upload   │
                    │  PDF / DOCX / TXT   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Document Parser    │
                    │ Text Extraction     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Text Chunking      │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │ Sentence Transformer           │
              │ all-MiniLM-L6-v2 (384D)        │
              └───────────────┬────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   FAISS Index       │
                    │   IndexFlatL2       │
                    └──────────┬──────────┘
                               │
                 User Question│
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    │ Top-K Relevant      │
                    │ Chunks              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Prompt Construction │
                    │ + Retrieved Context │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Groq LLM            │
                    │ Llama 3.3 70B       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Generated Resource  │
                    │ + Source Metadata   │
                    └─────────────────────┘

🤖 Core AI/ML Pipeline

1. Document Processing

Supported input formats:

PDF

DOCX

TXT

The application extracts text and prepares it for downstream retrieval.

2. Text Chunking

The extracted document is divided into smaller chunks so that relevant portions can be retrieved instead of sending the entire document to the LLM.

3. Semantic Embeddings

The application uses:

sentence-transformers/all-MiniLM-L6-v2

The model generates 384-dimensional embeddings for document chunks and user queries.

4. Vector Search

The embeddings are indexed using:

FAISS IndexFlatL2

The user query is embedded using the same model and searched against the document index to retrieve the most relevant chunks.

5. Retrieval-Augmented Generation

Retrieved chunks are injected into structured prompts before calling the LLM. This allows the application to generate answers and resources grounded in the uploaded document rather than relying only on the model's pretrained knowledge.

6. LLM Generation

The current MVP uses Groq API to access Llama 3.3 70B for generation.

💬 AI Question Answering

Teachers can ask natural-language questions about the uploaded document.

The question-answering workflow supports:

Document-grounded answers

Semantic retrieval

Top-K context selection

Teacher-friendly explanations

NCF 2023 / NEP 2020-oriented prompting

Explicit instructions to avoid unsupported facts

Web-search fallback when relevant document context is unavailable

Retrieval/source metadata

The RAG prompt explicitly instructs the model to use the uploaded document as the primary source and to state when requested information is not available in the retrieved material.

📚 Classroom Resource Generation

The MVP supports multiple document-grounded generation workflows.

📘 Study Notes

Generates resources such as:

Chapter overview

Learning outcomes

Competencies

Key concepts

Detailed notes

Revision notes

Real-life examples

Activity-based learning

Inclusive teaching strategy

Flow chart

Mind map

Summary

✅ MCQs

Supports assessment-oriented question generation including:

Single-correct-answer questions

Multiple-correct-answer questions

Assertion and reason

Case-based questions

Activity-based questions

Competency-based questions

Real-life scenarios

📝 Question Papers

Can generate question sets with:

Easy questions

Moderate questions

Difficult questions

Case-based questions

Activity-based questions

Competency mapping

Marks distribution

Answer keys

📋 Lesson Plans

Can generate structured lesson plans containing:

Curricular goals

Learning outcomes

Competency mapping

Teacher instructions/script

Student activities

Art-integrated learning

Game-based learning

Activity-based learning

Reflection activities

Assessment rubrics

Real-life applications

👨‍🏫 Teaching Guides

Can generate:

Teacher instructions

Student responses

Teaching strategies

Classroom activities

Common misconceptions

Assessments

Homework

Extension activities

🗺️ Visual Learning Resources

The application can generate text-based:

Mind maps

Flow charts

Concept structures

Chapter summaries

Important questions

🎯 NCF 2023 & NEP 2020 Focus

The prompting and resource-generation workflows are designed around educational principles such as:

Competency-based learning

Activity-based learning

Inclusive teaching

Inquiry-based learning

Critical thinking

Problem solving

Communication

Collaboration

Creativity

Art-integrated learning

Game-based learning

Real-life applications

Important: NCF 2023 / NEP 2020 alignment in this MVP is implemented primarily through the application's prompts, resource templates, and educational configuration. A complete machine-verifiable curriculum/NCF knowledge base is part of the future roadmap.

🔎 Explainable Retrieval & Metadata

The application records metadata associated with indexed document chunks, including:

Document name

Document ID

Document version

Page number when available

Chunk number

Total chunk count

Subject

Chapter

Word count

Character count

Embedding model

Embedding dimension

Retrieval method

Retrieval rank

Similarity value

Retrieval score

Retrieval timestamp

Upload timestamp

This metadata helps make the retrieval stage more transparent and makes the RAG pipeline easier to inspect and debug.

Retrieval scoring

The current MVP exposes multiple retrieval indicators, including FAISS L2 distance-derived similarity and a retrieval score.

Note: These values are retrieval/evaluation indicators, not calibrated probabilities that guarantee answer correctness.

📊 Document Intelligence Dashboard

After document ingestion, the interface displays information such as:

Document title

Subject

Chapter

Word count

Character count

Number of indexed chunks

Embedding model

Vector index status

Document status

Application version

Response-time statistics

Retrieval statistics during the session

📄 PDF Export

Generated educational resources can be exported as PDF using ReportLab.

The export functionality is designed to package generated classroom material together with available source/context information.

🧰 Technology Stack

Application

Python

Streamlit

Generative AI

Groq API

Llama 3.3 70B

NLP / Embeddings

Sentence Transformers

all-MiniLM-L6-v2

384-dimensional embeddings

Vector Search

FAISS

IndexFlatL2

Document Processing

PyPDF

python-docx

TXT processing

Web Search Fallback

Tavily Search API

PDF Generation

ReportLab

Supporting Libraries

NumPy

Pandas

Requests

Pillow

python-dotenv

📁 Project Structure

teacher-ai-assistant-main/
│
├── app.py                 # Streamlit application and UI workflow
├── config.py              # Application configuration
├── document_parser.py     # PDF/DOCX/TXT processing
├── chroma_manager.py      # FAISS embedding, indexing and retrieval utilities
├── rag_engine.py          # RAG question answering and context handling
├── generators.py          # Educational resource generation workflows
├── prompts.py             # LLM prompts and educational instructions
├── llm_service.py         # Groq LLM integration
├── pdf_generator.py       # PDF export functionality
├── intent_router.py       # Request/action routing
├── utils.py               # Utility and web-search functions
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

The filename chroma_manager.py is a legacy module name. In the current implementation, the module manages FAISS-based in-memory vector indexing, not a ChromaDB vector store.

⚙️ Local Setup

1. Clone the repository

git clone <your-repository-url>
cd teacher-ai-assistant-main

2. Create a virtual environment

python -m venv .venv

Windows

.venv\Scripts\activate

Linux / macOS

source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure API keys

Set the following environment variables or Streamlit secrets:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

Never commit real API keys, .env files, or Streamlit secrets to a public repository.

5. Run the application

streamlit run app.py

🚀 Deployment

The MVP is designed to run as a Streamlit application and has been deployed as a working web application.

For production deployment, additional infrastructure would be required for persistent document storage, user management, observability, caching, scalable vector storage, and background processing.

⚠️ Current MVP Limitations

This project is intentionally a Version 1.0 MVP. It should not be described as a fully production-grade enterprise platform yet.

Current limitations include:

FAISS index is maintained in Streamlit session state rather than a persistent managed vector database.

Uploaded document state is session-oriented.

User accounts and persistent chat history are not part of the current MVP.

There is no complete curriculum database covering every NCF 2023 subject and grade.

Retrieval scores are useful diagnostics but are not calibrated confidence probabilities.

LLM output can still contain errors and should be reviewed by educators.

Web search fallback introduces a second information source when the uploaded document does not provide sufficient context.

Multi-agent orchestration is not part of the current MVP.

These limitations define the boundary between the current prototype and the planned production architecture.

🗺️ Future Roadmap

Phase 2 — Enhanced Educational Intelligence

Planned improvements:

Expanded NCF 2023 knowledge base

Subject-wise competency mapping

Curriculum-goal alignment

Panchpadi learning framework

5E learning model

Bloom's Taxonomy integration

More structured curriculum validation

Phase 3 — Production Infrastructure

Potential additions:

Redis

For response caching, lower latency, and reduced repeated LLM calls.

PostgreSQL / Supabase

For:

User accounts

Persistent chat history

Saved resources

Document management

Analytics

Persistent Vector Storage

Move beyond session-based FAISS indexing toward persistent and scalable vector infrastructure.

LangGraph

For multi-step educational workflows and agent orchestration.

MCP

For future integration with external educational systems, APIs, and tools.

Phase 4 — Multi-Agent Educational System

Potential specialized agents:

Curriculum Agent

Lesson Planning Agent

Assessment Agent

Teaching Strategy Agent

Inclusive Education Agent

Classroom Activity Agent

Student Performance Analysis Agent

🧪 Example End-to-End Flow

1. Teacher uploads a PDF
          ↓
2. Application extracts document text
          ↓
3. Text is divided into chunks
          ↓
4. Sentence Transformer creates 384D embeddings
          ↓
5. FAISS builds an in-memory vector index
          ↓
6. Teacher enters a topic/question
          ↓
7. Query is converted into an embedding
          ↓
8. FAISS retrieves the most relevant chunks
          ↓
9. Retrieved context is inserted into an educational prompt
          ↓
10. Groq/Llama 3.3 70B generates the response
          ↓
11. Application displays the generated resource
          ↓
12. Retrieval/source metadata is available for inspection

💡 Key AI/ML Concepts Demonstrated

This project demonstrates practical implementation of:

Retrieval-Augmented Generation (RAG)

Natural Language Processing

Semantic Search

Text Embeddings

Vector Similarity Search

FAISS indexing

Prompt Engineering

Context Injection

LLM API Integration

Document Intelligence

Source Traceability

Retrieval Diagnostics

Generative AI application development

Streamlit deployment

🎓 Assessment / Portfolio Value

This project is particularly relevant for roles and assessments involving:

AI/ML Engineering

Generative AI

NLP

Data Science

LLM Applications

RAG Systems

AI Application Development

Prompt Engineering

Python Development

The project demonstrates an end-to-end AI application rather than a standalone model or simple API call.

🎯 Vision

The long-term goal is to evolve this MVP into an AI Teacher Copilot that provides grounded, explainable, curriculum-aware assistance to educators.

The planned evolution moves from a session-based RAG prototype toward a more scalable system with persistent knowledge, user workspaces, curriculum intelligence, workflow orchestration, and specialized educational agents.

👨‍💻 Built With

Python

Streamlit

Groq

Llama 3.3 70B

FAISS

Sentence Transformers

all-MiniLM-L6-v2

ReportLab

Tavily

NCF 2023 principles

NEP 2020 principles

📌 Project Status

Version 1.0 MVP — Working RAG-based Generative AI application

The current release focuses on demonstrating the complete document-to-retrieval-to-generation workflow. Production-scale persistence, authentication, advanced curriculum intelligence, and multi-agent orchestration are planned for future versions.
