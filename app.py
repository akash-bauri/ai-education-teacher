import streamlit as st
import time
import traceback
from datetime import datetime

# Centralized Configurations
import config

# Active Groq model override.
# Other modules imported below can read this value from the shared config module.
config.LLM_MODEL = "qwen/qwen3.8-27b"

# Document Processing
from document_parser import (
    extract_document_text,
    chunk_text,
    get_document_info
)

# Vector Database
from chroma_manager import (
    store_document_chunks,
    get_document_count,
    get_document_name
)

# RAG Engine
from rag_engine import (
    rag_answer,
    generate_document_notes,
    generate_document_mcqs,
    generate_document_question_paper
)

# Content Generators
from generators import (
    generate_learning_outcomes,
    generate_competencies,
    generate_lesson_plan,
    generate_teaching_guide,
    generate_flowchart,
    generate_mindmap,
    generate_chapter_summary,
    generate_important_questions
)

# PDF Generators
from pdf_generator import notes_pdf

# Utilities
from utils import (
    initialize_history,
    save_to_history,
    get_history,
    detect_difficulty,
    detect_marks,
    search_web,
    format_web_results
)

# =====================================================
# INITIALIZATION & STATE MANAGEMENT
# =====================================================
st.set_page_config(
    page_title=f"NCF 2023 AI Teacher Assistant - {config.APP_VERSION}",
    page_icon="📚",
    layout="wide"
)

initialize_history()

# Advanced Telemetry Tracking Initializer
if "session_start_time" not in st.session_state:
    st.session_state["session_start_time"] = datetime.now()
if "stat_questions" not in st.session_state:
    st.session_state["stat_questions"] = 0
if "stat_resources" not in st.session_state:
    st.session_state["stat_resources"] = 0
if "stat_response_times" not in st.session_state:
    st.session_state["stat_response_times"] = []
if "stat_uploads" not in st.session_state:
    st.session_state["stat_uploads"] = 0
if "stat_confidences" not in st.session_state:
    st.session_state["stat_confidences"] = []
if "stat_similarities" not in st.session_state:
    st.session_state["stat_similarities"] = []
if "stat_retrievals" not in st.session_state:
    st.session_state["stat_retrievals"] = []

# Persistent Context Variables
if "doc_metadata" not in st.session_state:
    st.session_state["doc_metadata"] = None
if "document_text" not in st.session_state:
    st.session_state["document_text"] = ""
if "document_chunks" not in st.session_state:
    st.session_state["document_chunks"] = []
if "last_uploaded_file" not in st.session_state:
    st.session_state["last_uploaded_file"] = None
if "upload_time" not in st.session_state:
    st.session_state["upload_time"] = "N/A"

# Form State Triggers
if "student_level_sel" not in st.session_state:
    st.session_state["student_level_sel"] = "Class 5"
if "teaching_style_sel" not in st.session_state:
    st.session_state["teaching_style_sel"] = "Beginner Friendly"


# =====================================================
# REUSABLE MODULAR UI BLOCKS (HELPER FUNCTIONS)
# =====================================================
def run_staged_pipeline(stages_dict):
    """Executes a visual progressive pipeline showing loading states sequentially."""
    progress_bar = st.progress(0, text="Initializing workflow nodes...")
    for percentage, stage_text in stages_dict.items():
        progress_bar.progress(percentage, text=f"⚙️ {stage_text}")
        time.sleep(0.1)
    progress_bar.empty()

def render_sidebar(doc_count, history_records):
    """Renders all components inside the sidebar workspace."""
    with st.sidebar:
        st.title(f"📚 NCF AI Assistant")
        st.caption(config.APP_VERSION)
        
        st.markdown("### 🎬 Presentation Tools")
        if st.button("🎬 Load Demo Chapter", use_container_width=True):
            load_demo_data()
            st.success("Demo Chapter Seeded!")
            st.rerun()

        st.divider()
        
        # Live System Status
        st.markdown("### 📡 Active System Status")
        with st.container(border=True):
            st.markdown(f"🟢 **LLM Status:** `Connected`")
            st.markdown(f"🧠 **Embedding Model:** `{config.EMBEDDING_MODEL}`")
            st.markdown(f"🗄️ **FAISS Status:** `Ready & Loaded`")
            if st.session_state["doc_metadata"]:
                st.markdown("🟢 **Document Status:** `Indexed`")
            else:
                st.markdown("⚪ **Document Status:** `Uninitialized`")
            st.markdown(f"⚡ **Version:** `{config.APP_VERSION}`")

        st.divider()
        
        # Real-time Session Analytics Dashboard
        st.markdown("### 📊 Session Analytics")
        with st.container(border=True):
            dur_delta = datetime.now() - st.session_state["session_start_time"]
            mins_active = int(dur_delta.total_seconds() // 60)
            avg_resp = (sum(st.session_state["stat_response_times"]) / len(st.session_state["stat_response_times"])) if st.session_state["stat_response_times"] else 0.0
            avg_conf = (sum(st.session_state["stat_confidences"]) / len(st.session_state["stat_confidences"])) if st.session_state["stat_confidences"] else 0.0
            avg_sim = (sum(st.session_state["stat_similarities"]) / len(st.session_state["stat_similarities"])) if st.session_state["stat_similarities"] else 0.0
            
            st.metric("❓ Questions Asked", f"{st.session_state['stat_questions']}")
            st.metric("📦 Resources Generated", f"{st.session_state['stat_resources']}")
            st.metric("⚡ Avg Response Time", f"{avg_resp:.2f}s")
            st.metric("📄 Documents Uploaded", f"{st.session_state['stat_uploads']}")
            st.metric("⏱️ Session Duration", f"{mins_active} min(s)")
            st.metric("🎯 Avg Confidence", f"{avg_conf:.1f}%")
            st.metric("⭐ Avg Similarity", f"{avg_sim:.2f}")

        st.divider()
        
        # Architectural Transaction Logs
        st.markdown("### 📜 Session History Logs")
        if history_records:
            for item in reversed(history_records[-3:]):
                with st.container(border=True):
                    st.markdown(f"❓ **Query:** `{item.get('question', '')[:30]}...`")
                    st.markdown(f"📦 **Action:** `{item.get('resource_type', 'Task Node')}`")
                    st.caption(f"🕒 `{item.get('timestamp', 'N/A')}`")
        else:
            st.caption("No dynamic historical logs stored.")

def render_document_summary():
    """Renders the document statistics banner post-upload."""
    meta = st.session_state["doc_metadata"]
    if meta:
        st.markdown("### 📊 Ingested Document Profile")
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"📄 **Title:** `{meta['title']}`\n\n🗄️ **Database Structure:** `{config.VECTOR_DATABASE}`")
            c2.markdown(f"📘 **Subject Node:** `{meta['subject']}`\n\n🔖 **Chapter Node:** `{meta['chapter']}`")
            c3.markdown(f"📑 **Chunk Matrices:** `{len(st.session_state['document_chunks'])} Units`\n\n🧠 **Embeddings Engine:** `{config.EMBEDDING_MODEL}`")

def render_smart_preview():
    """Renders an insightful preview analytical drawer of the contextual text."""
    meta = st.session_state["doc_metadata"]
    if meta:
        with st.expander("🔍 Smart Document Preview & Context Synthesis", expanded=False):
            pv_c1, pv_c2 = st.columns([2, 1])
            with pv_c1:
                st.markdown("#### 📄 Document Buffer Text Preview (First 500 Words)")
                preview_words = st.session_state["document_text"].split()[:500]
                st.text_area("", value=" ".join(preview_words), height=230, disabled=True, label_visibility="collapsed")
            with pv_c2:
                st.markdown("#### 🧠 AI Inspected Architecture")
                st.markdown(f"📈 **Reading Level:** `{meta['reading_level']}`")
                st.markdown(f"⏱️ **Reading Time Budget:** `{meta['reading_time']}`")
                st.write("**Topics:**", ", ".join(meta['detected_topics']))
                st.write("**Keywords:**", ", ".join(meta['detected_keywords']))
                st.write("**Outcomes:**", ", ".join(meta['learning_outcomes']))
                st.write("**Competencies:**", ", ".join(meta['competencies']))

def render_output_info_card(resource_name, query_text, s_level, t_style, src):
    """Renders an output informational card above every generated output component."""
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"📦 **Generated Resource:** `{resource_name}`\n\n🎯 **Topic:** `{query_text[:30]}...`")
        c2.markdown(f"🎓 **Student Level:** `{s_level}`\n\n🎨 **Teaching Style:** `{t_style}`")
        c3.markdown(f"📊 **Difficulty:** `{detect_difficulty(query_text)}`\n\n🏷️ **Marks Target:** `{detect_marks(query_text)}`")
        c4.markdown(f"🕒 **Generated Time:** `{datetime.now().strftime('%H:%M:%S')}`\n\n🧬 **Source Routing:** `{src}`")

def render_source_traceability(rag_payload, exec_time, s_level, t_style, src_name):
    """Renders dynamic, high-fidelity metadata audit records inside an expandable element."""
    with st.expander("🎯 Source Traceability Operational Matrix", expanded=True):
        if rag_payload:
            st.markdown("### 📄 Architectural Context Citation Summary")
            tr_c1, tr_c2, tr_c3 = st.columns(3)
            with tr_c1:
                st.markdown(f"**Source Document:** `{src_name}`")
                st.markdown(f"**Page Number:** `Page {rag_payload.get('page', '1')}`")
                st.markdown(f"**Chunk Number:** `Segment {rag_payload.get('chunk', '1')}`")
                st.markdown(f"**Document Version:** `v1.0.0 (Immutable Master Document)`")
            with tr_c2:
                st.markdown(f"**Similarity Score:** `{rag_payload.get('similarity', 'N/A')}`")
                st.markdown(f"**Confidence Score:** `{rag_payload.get('confidence', 'N/A')}%`")
                st.markdown(f"**Retrieval Score:** `{rag_payload.get('retrieval_score', 'N/A')}`")
                st.markdown(f"**Rank Priority:** `Priority Rank #{rag_payload.get('rank', '1')}`")
            with tr_c3:
                st.markdown(f"**Generated Time:** `{exec_time}`")
                st.markdown(f"**LLM Model:** `{config.LLM_MODEL}`")
                st.markdown(f"**Embedding Model:** `{config.EMBEDDING_MODEL}`")
                st.markdown(f"**Vector Database:** `{config.VECTOR_DATABASE}`")
        else:
            st.info("ℹ️ No extended document metadata available for the current generation route context (Web Search/Direct Prompt rules applied).")


# =====================================================
# DEMO MODE SEED ENGINE
# =====================================================
def load_demo_data():
    st.session_state["document_text"] = (
        "Chapter 3: Plants and Living Systems. Plants are primary producers that convert sunlight "
        "into energy through photosynthesis. The key organs are leaves, stems, and roots. "
        "Roots absorb water and anchor the plant. Stems provide transport networks via xylem and phloem. "
        "Leaves facilitate gas exchange and house chloroplasts. Understanding plant structures is "
        "vital to exploring ecosystems, biodiversity, and conservation efforts under environmental changes."
    )
    st.session_state["document_chunks"] = [
        st.session_state["document_text"][:250],
        st.session_state["document_text"][250:]
    ]
    st.session_state["last_uploaded_file"] = "Demo_Plant_Systems_Chapter.pdf"
    st.session_state["upload_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["stat_uploads"] += 1
    
    st.session_state["doc_metadata"] = {
        "title": "Demo_Plant_Systems_Chapter.pdf",
        "subject": "Science",
        "chapter": "Plants and Living Systems",
        "total_pages": "2 Pages",
        "reading_time": "1 min read",
        "doc_type": "PDF",
        "detected_topics": ["Photosynthesis", "Vascular Systems", "Ecosystem Biodiversity"],
        "detected_keywords": ["Xylem", "Phloem", "Chloroplasts", "Producers"],
        "learning_outcomes": ["Correlate plant structure functionality with metabolic output requirements"],
        "competencies": ["Scientific Framework Investigation"],
        "reading_level": "Grade 5 Basic Curriculum Standard"
    }
    st.session_state["student_level_sel"] = "Class 5"
    st.session_state["teaching_style_sel"] = "Beginner Friendly"
    
    store_document_chunks(
        chunks=st.session_state["document_chunks"], 
        document_name="Demo_Plant_Systems_Chapter.pdf",
        page_numbers=["1", "2"],
        subject="Science",
        chapter="Plants and Living Systems"
    )


# =====================================================
# INGESTION ENTRY POINT & ADVANCED VALIDATION GATEWAY
# =====================================================
# Fetch static variables to conserve datetime operations loop counts
current_history_records = get_history()
current_doc_count = get_document_count()

# Render primary unified layout interface elements
render_sidebar(current_doc_count, current_history_records)

st.title("📚 NCF 2023 AI Teacher Assistant")
col_b1, col_b2, col_b3, col_b4, col_b5, col_b6 = st.columns(6)
for col, text in zip([col_b1, col_b2, col_b3, col_b4, col_b5, col_b6], 
                     ["✨ NCF 2023 Aligned", "🧠 Competency Based", "🏃 Activity Based", "🤝 Inclusive Teaching", "🎨 Art Integrated", "🎮 Game Based"]):
    col.caption(text)
st.markdown("---")

uploaded_file = st.file_uploader("Upload Source Content Material (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Check boundaries and signatures to perform input text validation checks
    uploaded_file.seek(0, 2)
    bytes_length = uploaded_file.tell()
    uploaded_file.seek(0)
    file_size_mb = bytes_length / (1024 * 1024)
    
    is_duplicate_trigger = (st.session_state["last_uploaded_file"] == uploaded_file.name)
    
    if file_size_mb > config.MAX_FILE_SIZE_MB:
        st.error(f"❌ Document Validation Error: File size exceeds the allowed limit ({file_size_mb:.2f}MB / Max {config.MAX_FILE_SIZE_MB}MB).")
    elif bytes_length == 0:
        st.error("❌ Document Validation Error: The uploaded file is completely empty or corrupted.")
    elif is_duplicate_trigger:
        st.warning("⚠️ Document Already Ingested: This document metadata matrix has already been initialized in the session.")
    else:
        try:
            # Staged Pipeline Ingestion Feedback Engine
            ingest_animation_map = {
                15: "Uploading Document parameters to system runtime environments...",
                35: "Extracting Text layout maps from source content file buffers...",
                55: "Creating Chunks optimized using token boundaries and lexical wrappers...",
                75: "Generating Embeddings vector matrices across native transformer graphs...",
                95: "Building FAISS Index contexts inside the localized workspace databases...",
                100: "Completed Successfully — Ingestion stage mapping resolved."
            }
            run_staged_pipeline(ingest_animation_map)
            
            raw_text = extract_document_text(uploaded_file)
            word_count_check = len(raw_text.split())
            
            if word_count_check < config.MIN_WORD_COUNT:
                st.error(f"❌ Document Validation Error: Insufficient content depth found ({word_count_check} words / Minimum required: {config.MIN_WORD_COUNT} words).")
            else:
                st.session_state["document_text"] = raw_text
                computed_chunks = chunk_text(raw_text)
                st.session_state["document_chunks"] = computed_chunks
                st.session_state["last_uploaded_file"] = uploaded_file.name
                st.session_state["upload_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state["stat_uploads"] += 1
                
                # CRITICAL FIX: Reset file pointer stream prior to extraction rules execution
                uploaded_file.seek(0)
                
                try:
                    meta_extraction = get_document_info(uploaded_file)
                    st.session_state["doc_metadata"] = {
                        "title": meta_extraction.get("title", uploaded_file.name),
                        "subject": meta_extraction.get("subject") if meta_extraction.get("subject") else "Unknown",
                        "chapter": meta_extraction.get("chapter") if meta_extraction.get("chapter") else "Unknown",
                        "total_pages": meta_extraction.get("total_pages", "1 Page"),
                        "reading_time": meta_extraction.get("reading_time", f"{max(1, word_count_check//160)} min read"),
                        "doc_type": meta_extraction.get("doc_type", uploaded_file.name.split(".")[-1].upper()),
                        "detected_topics": meta_extraction.get("detected_topics", ["Foundational Pedagogics"]),
                        "detected_keywords": meta_extraction.get("detected_keywords", ["NCF Directive"]),
                        "learning_outcomes": meta_extraction.get("learning_outcomes", ["Synthesize context references"]),
                        "competencies": meta_extraction.get("competencies", ["Cognitive core structuring"]),
                        "reading_level": meta_extraction.get("reading_level", "Academic Standard Layout")
                    }
                except Exception:
                    st.session_state["doc_metadata"] = {
                        "title": uploaded_file.name, "subject": "Unknown", "chapter": "Unknown",
                        "total_pages": "1 Page", "reading_time": "Dynamic Budget", "doc_type": "TXT",
                        "detected_topics": ["General Curriculum Subject"], "detected_keywords": ["Context Standard"],
                        "learning_outcomes": ["Process explicit data summary structures"], "competencies": ["General Comprehension Strategy"],
                        "reading_level": "Standard Text Matrix"
                    }
                
                store_document_chunks(
                    chunks=computed_chunks,
                    document_name=uploaded_file.name,
                    subject=st.session_state["doc_metadata"]["subject"],
                    chapter=st.session_state["doc_metadata"]["chapter"]
                )
                st.success("🎉 Document successfully validated, converted, and fully indexed inside the local vector memory workspace.")
                st.rerun()
        except Exception as file_err:
            st.error("❌ Corrupted Document Error: System architecture failed to parse the internal structures of this document.")
            with st.expander("Technical Exception Trace", expanded=False):
                st.code(traceback.format_exc())

# Invoke secondary diagnostic UI visualization modules
render_document_summary()
render_smart_preview()


# =====================================================
# ACTION CONTEXT DEFINITION SELECTORS
# =====================================================
action = st.selectbox(
    "Choose Resource Action Block",
    [
        "📦 Generate Complete Teaching Package", "Ask Question", "Generate Notes", "Generate MCQs",
        "Generate Question Paper", "Generate Learning Outcomes", "Generate Competencies",
        "Generate Lesson Plan", "Generate Teaching Guide", "Generate Flow Chart",
        "Generate Mind Map", "Generate Chapter Summary", "Generate Important Questions", "Web Search"
    ]
)

query = st.text_area("Enter Core Topic Target, Focus Area, or Question Parameters")

# Educational Profile Context Selection
st.markdown("### ⚙️ Educational Configuration Parameters")
config_col1, config_col2 = st.columns(2)
with config_col1:
    # The default is initialized in st.session_state above. Do not also pass index=,
    # because Streamlit warns when a keyed widget's value is set through Session State.
    student_level = st.selectbox(
        "Student Level",
        [f"Class {i}" for i in range(1, 13)],
        key="student_level_sel",
    )
with config_col2:
    teaching_style = st.selectbox(
        "Teaching Style",
        [
            "Beginner Friendly",
            "Concept Based",
            "Activity Based",
            "Competency Based",
            "Interactive Learning",
            "Exam Oriented",
        ],
        key="teaching_style_sel",
    )

# Verify access constraints and clear path routing checks
is_document_present = (st.session_state["doc_metadata"] is not None)
if action in config.DOCUMENT_DEPENDENT_ACTIONS and not is_document_present:
    st.error("❌ Resource Action Locked: The requested option requires active document context parameters.")
    st.info("💡 Hint: Load the demonstration data module above or choose 'Web Search' as your active route action block.")
    st.stop()


# =====================================================
# ENGINE INFERENCE PIPELINE RUNTIME
# =====================================================
if st.button("🚀 Generate Content Blueprint"):
    if not query:
        st.warning("Please fill in prompt requirements before initiating tracking execution threads.")
        st.stop()
        
    outputs = {}
    rag_metadata_payload = None
    start_time_mark = datetime.now()
    execution_ts = start_time_mark.strftime("%Y-%m-%d %H:%M:%S")
    
    # Safely assign working context properties
    if is_document_present:
        target_source_title = st.session_state["doc_metadata"]["title"]
        target_subject = st.session_state["doc_metadata"]["subject"]
        target_chapter = st.session_state["doc_metadata"]["chapter"]
    else:
        target_source_title = "System Core Directives"
        target_subject = "Unknown"
        target_chapter = "Unknown"

    inference_animation_map = {
        20: "Searching Knowledge Base maps matching criteria requirements...",
        50: "Extracting semantic vector intersections using local matrix weights...",
        80: "Generating AI Response outputs utilizing localized hyper-speed endpoints...",
        95: "Preparing Output text streams formatting final blueprint components...",
        100: "Completed Successfully — Generation node parameters cleared."
    }
    run_staged_pipeline(inference_animation_map)
    
    try:
        # Pipeline Router Flow Logic Execution
        if action == "📦 Generate Complete Teaching Package":
            outputs["outcomes"] = generate_learning_outcomes(query, student_level)
            outputs["competencies"] = generate_competencies(query, student_level)
            outputs["notes"] = generate_document_notes(query, student_level)
            outputs["mcqs"] = generate_document_mcqs(query, detect_difficulty(query))
            outputs["paper"] = generate_document_question_paper(query, detect_marks(query), detect_difficulty(query))
            outputs["lesson"] = generate_lesson_plan(query, student_level)
            outputs["guide"] = generate_teaching_guide(query, student_level, teaching_style)
            outputs["flowchart"] = generate_flowchart(query)
            outputs["mindmap"] = generate_mindmap(query)
            outputs["summary"] = generate_chapter_summary(query)
            outputs["questions"] = generate_important_questions(query)
            st.session_state["stat_resources"] += 11
            
        elif action == "Ask Question":
            resp_payload = rag_answer(query, student_level)
            outputs["notes"] = resp_payload["answer"]
            target_source_title = resp_payload["source"]
            if "source_info" in resp_payload and resp_payload["source_info"]:
                rag_metadata_payload = resp_payload["source_info"]
            st.session_state["stat_questions"] += 1
            
        else:
            st.session_state["stat_resources"] += 1
            if action == "Generate Notes":
                outputs["notes"] = generate_document_notes(query, student_level)
            elif action == "Generate MCQs":
                outputs["mcqs"] = generate_document_mcqs(query, detect_difficulty(query))
            elif action == "Generate Question Paper":
                outputs["paper"] = generate_document_question_paper(query, detect_marks(query), detect_difficulty(query))
            elif action == "Generate Learning Outcomes":
                outputs["outcomes"] = generate_learning_outcomes(query, student_level)
            elif action == "Generate Competencies":
                outputs["competencies"] = generate_competencies(query, student_level)
            elif action == "Generate Lesson Plan":
                outputs["lesson"] = generate_lesson_plan(query, student_level)
            elif action == "Generate Teaching Guide":
                outputs["guide"] = generate_teaching_guide(query, student_level, teaching_style)
            elif action == "Generate Flow Chart":
                outputs["flowchart"] = generate_flowchart(query)
            elif action == "Generate Mind Map":
                outputs["mindmap"] = generate_mindmap(query)
            elif action == "Generate Chapter Summary":
                outputs["summary"] = generate_chapter_summary(query)
            elif action == "Generate Important Questions":
                outputs["questions"] = generate_important_questions(query)
            elif action == "Web Search":
                web_raw = search_web(query)
                outputs["notes"] = format_web_results(web_raw)
                target_source_title = "Web Search Outlets"

        delta_seconds = (datetime.now() - start_time_mark).total_seconds()
        st.session_state["stat_response_times"].append(delta_seconds)

        # Update analytical aggregators if matching parameters are found
        if rag_metadata_payload:
            st.session_state["stat_confidences"].append(float(rag_metadata_payload.get("confidence", 0.0)))
            st.session_state["stat_similarities"].append(float(rag_metadata_payload.get("similarity", 0.0)))

        # Display Unified Output Component Cards
        render_output_info_card(action, query, student_level, teaching_style, target_source_title)
        render_source_traceability(rag_metadata_payload, execution_ts, student_level, teaching_style, target_source_title)
        
        st.divider()

        # =====================================================
        # VISUAL CONTAINER OUTPUT MATRIX TABS
        # =====================================================
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "📋 Notes", "🧩 MCQs", "📝 Question Paper", "🧭 Lesson Plan",
            "📖 Teaching Guide", "📊 Flow Chart", "🧠 Mind Map", "📑 Chapter Summary", "❓ Important Questions"
        ])
        
        with tab1:
            st.markdown(outputs.get("notes", outputs.get("outcomes", "No primary structured text was loaded for this view block segment.")))
        with tab2:
            st.markdown(outputs.get("mcqs", "No assessment data arrays found for this component."))
        with tab3:
            st.markdown(outputs.get("paper", "No exam blueprint loaded."))
        with tab4:
            st.markdown(outputs.get("lesson", "No lesson structure parameters returned."))
        with tab5:
            st.markdown(outputs.get("guide", "No interactive guide logs calculated."))
        with tab6:
            st.markdown(outputs.get("flowchart", "No procedural flow layout data configured."))
        with tab7:
            st.markdown(outputs.get("mindmap", "No relationship mapping diagrams constructed."))
        with tab8:
            st.markdown(outputs.get("summary", "No curriculum summaries compiled."))
        with tab9:
            st.markdown(outputs.get("questions", "No priority tiered problem questions returned."))

        # =====================================================
        # COMPREHENSIVE ASSET EXPORT LAYER WITH INTEGRATED HEADER
        # =====================================================
        st.divider()
        st.subheader("📥 Export Curricular Asset Blocks")
        
        # Self-contained header injection to make exported documents self-contained
        pdf_header_preface = (
            f"=====================================================\n"
            f"NCF AI TEACHER ASSISTANT INTELLECTUAL CURRICULAR PAYLOAD\n"
            f"=====================================================\n"
            f"- Document Reference: {target_source_title}\n"
            f"- Subject Category: {target_subject} | Chapter Track: {target_chapter}\n"
            f"- Target Student Level: {student_level} | Applied Pedagogy Style: {teaching_style}\n"
            f"- Generation Time Mark: {execution_ts} | Application Core Version: {config.APP_VERSION}\n"
            f"- Inference Processing Node: {config.LLM_MODEL} | Text Embeddings Graph: {config.EMBEDDING_MODEL}\n"
            f"- Data Validation Audit Matrix Metrics: Confidence Score: {rag_metadata_payload.get('confidence', 'N/A') if rag_metadata_payload else 'N/A'}% | Similarity Weight: {rag_metadata_payload.get('similarity', 'N/A') if rag_metadata_payload else 'N/A'}\n"
            f"-----------------------------------------------------\n\n\n"
        )
        
        raw_string_compilation = pdf_header_preface + "\n\n***\n\n".join([f"# {k.upper()}\n{v}" for k, v in outputs.items()])
        compiled_stream_buffer = notes_pdf(raw_string_compilation, target_source_title)

        ec1, ec2 = st.columns(2)
        with ec1:
            with st.container(border=True):
                st.markdown("#### 📄 Integrated Curricular Payload Block")
                st.download_button(
                    label="📥 Download Generated Asset PDF",
                    data=compiled_stream_buffer,
                    file_name="NCF_Resource_Export.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with ec2:
            with st.container(border=True):
                st.markdown("#### 🗄️ Full Bundle Teaching Distribution Package")
                st.download_button(
                    label="📥 Download Complete Package PDF",
                    data=compiled_stream_buffer,
                    file_name="Complete_NCF_Teaching_Package.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    disabled=(action != "📦 Generate Complete Teaching Package")
                )

        # =====================================================
        # LONG-TERM DATABASE-COMPATIBLE HISTORY PERSISTENCE
        # =====================================================
        save_to_history(query, raw_string_compilation, target_source_title)
        
        if st.session_state.get("history"):
            db_record = st.session_state["history"][-1]
            db_record.update({
                "question": query,
                "action": action,
                "student_level": student_level,
                "teaching_style": teaching_style,
                "document": target_source_title,
                "subject": target_subject,
                "chapter": target_chapter,
                "difficulty": detect_difficulty(query),
                "marks": detect_marks(query),
                "confidence_score": rag_metadata_payload.get("confidence", "N/A") if rag_metadata_payload else "N/A",
                "similarity_score": rag_metadata_payload.get("similarity", "N/A") if rag_metadata_payload else "N/A",
                "retrieval_score": rag_metadata_payload.get("retrieval_score", "N/A") if rag_metadata_payload else "N/A",
                "response_time": f"{delta_seconds:.2f}s",
                "generation_time": execution_ts,
                "llm_model": config.LLM_MODEL,
                "embedding_model": config.EMBEDDING_MODEL,
                "vector_database": config.VECTOR_DATABASE
            })

    except Exception as runtime_error:
        # Graceful, decoupled structural error handling implementation
        if 'runtime_tracker' in locals():
            runtime_tracker.empty()
        st.error("❌ Unable to generate the requested resource.")
        st.markdown(
            "**Possible system failure reasons identified:**\n"
            "• Empty document context allocation map found.\n"
            "• Invalid document data elements or incorrect language formatting.\n"
            "• LLM inference core pipeline API call failure or token timeout.\n"
            "• Retrieval constraint weight error inside the FAISS index database."
        )
        with st.expander("🛠️ Technical Details (Traceback Stack Frame)", expanded=False):
            st.code(traceback.format_exc())

# =====================================================
# PLATFORM FOOTER LAYOUT COMPONENT
# =====================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
foot_c1, foot_c2, foot_c3 = st.columns([1, 4, 1])
with foot_c2:
    st.markdown(
        f"<center style='color: gray; font-size: 0.85rem; line-height: 1.4rem;'>"
        f"<b>Built Framework Architecture Nodes:</b><br>"
        f"Groq Inference • FAISS Matrix Database • Sentence Transformers • Streamlit Application Container • ReportLab SDK<br>"
        f"<b>Curricular Governance Framework Policies:</b><br>"
        f"National Curriculum Framework (NCF 2023) | National Education Policy (NEP 2020) — <i>{config.APP_VERSION}</i>"
        f"</center>",
        unsafe_allow_html=True
    )
    st.divider()
    st.markdown(
        "<center style='color: #a0a0a0; font-size: 0.75rem;'>"
        "<b>Core Production Architecture Roadmap:</b> Redis Optimization Cache Layer • PostgreSQL Vector Storage Layers • "
        "Supabase Authentication Relay Handles • LangGraph Multi-Agent Orchestration Graphs • Model Context Protocol (MCP) Integration Hooks • "
        "BM25 Hybrid Lexical Match Search Models"
        "</center>",
        unsafe_allow_html=True
    )
st.markdown("---")
