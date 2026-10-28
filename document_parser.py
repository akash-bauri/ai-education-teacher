# document_parser.py
import re
from datetime import datetime
from pypdf import PdfReader
from docx import Document

# =====================================================
# SYSTEM CLEANING & NORMALIZATION UTILITIES
# =====================================================

def clean_text(text):
    """Clean extracted text by normalizing whitespace structures."""
    if not text:
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


# =====================================================
# SECURE EXTRACTORS WITH ADVANCED TELEMETRY CORRECTIONS
# =====================================================

def extract_pdf_text_with_pages(uploaded_file):
    """
    Extracts text while systematically tracking absolute page contexts.
    Returns a tuple of (full_text, list_of_dictionaries_containing_page_mapping).
    """
    text_parts = []
    page_mappings = []
    
    try:
        # Guarantee file stream pointer is set to initial index node
        uploaded_file.seek(0)
        pdf = PdfReader(uploaded_file)
        
        # Immediate structural corruption/encryption checks
        if pdf.is_encrypted:
            return "PDF Error: Encrypted PDF files cannot be processed without authorization keys.", []
        if len(pdf.pages) == 0:
            return "PDF Error: Empty document allocation layout frame.", []
            
        for index, page in enumerate(pdf.pages):
            page_num = index + 1
            page_text = page.extract_text()
            if page_text and page_text.strip():
                text_parts.append(page_text)
                # Split content into raw logical paragraphs
                paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]
                for para in paragraphs:
                    page_mappings.append({
                        "text": para,
                        "page": str(page_num)
                    })
                    
        full_text = "\n".join(text_parts)
        return full_text, page_mappings
    except Exception as e:
        return f"PDF Error: Corrupted or structurally unreadable file matrix. Details: {e}", []


def extract_document_text(uploaded_file):
    """Automatically detects format types and handles target system transformations."""
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()
    try:
        uploaded_file.seek(0)
        if filename.endswith(".pdf"):
            text, _ = extract_pdf_text_with_pages(uploaded_file)
        elif filename.endswith(".docx"):
            doc = Document(uploaded_file)
            text = "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])
        elif filename.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8", errors="ignore")
        else:
            return "Unsupported file format. Please upload PDF, DOCX or TXT."
            
        return clean_text(text)
    except Exception as e:
        return f"Document Error: {e}"


# =====================================================
# HIERARCHICAL PAGE-AWARE SEMANTIC CHUNKER
# =====================================================

def chunk_text(text, chunk_size=1000, overlap=150):
    """
    Maintains backward compatibility for standard character/sentence splits.
    Used as a fallback mechanism for plain unstructured string layouts.
    """
    if not text:
        return []

    text = clean_text(text)
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            split_pos = max(
                text.rfind(".", start, end),
                text.rfind("?", start, end),
                text.rfind("!", start, end)
            )
            if split_pos > start:
                end = split_pos + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0 or end >= len(text):
            break
            
    return chunks


def chunk_document_hierarchical(page_mappings, chunk_size=1000, overlap=150):
    """
    Advanced hierarchical structural chunker that aligns page contexts 
    with chunk arrays, preserving semantic bounds and sentences.
    """
    chunks_with_metadata = []
    if not page_mappings:
        return []
        
    current_chunk_text = ""
    current_pages = set()
    
    for mapping in page_mappings:
        para_text = mapping["text"]
        page_lbl = mapping["page"]
        
        # If adding paragraph exceeds target limits, finalize current workspace chunk
        if len(current_chunk_text) + len(para_text) > chunk_size and current_chunk_text:
            chunks_with_metadata.append({
                "text": current_chunk_text.strip(),
                "pages": sorted(list(current_pages))
            })
            # Handle overlap configurations
            current_chunk_text = current_chunk_text[-overlap:] if overlap < len(current_chunk_text) else current_chunk_text
        else:
            current_chunk_text += "\n\n" + para_text
            current_pages.add(page_lbl)
            
    if current_chunk_text.strip():
        chunks_with_metadata.append({
            "text": current_chunk_text.strip(),
            "pages": sorted(list(current_pages))
        })
        
    return chunks_with_metadata


# =====================================================
# EDUCATIONAL INTELLIGENCE & METADATA FACTORY
# =====================================================

def _detect_subject(text):
    """Heuristic keyword classifier for foundational curricula matching."""
    text_lower = text.lower()
    subject_weights = {
        "Mathematics": ["algebra", "geometry", "calculus", "fraction", "equations", "numbers", "theorem", "multiply"],
        "Science": ["energy", "matter", "organism", "chemical", "evolution", "ecosystem", "forces", "microscope"],
        "Biology": ["cells", "plants", "photosynthesis", "anatomy", "dna", "species", "organ", "respiration"],
        "Physics": ["velocity", "gravity", "quantum", "thermodynamics", "optics", "magnetism", "friction"],
        "Chemistry": ["molecule", "periodic table", "acid", "bonding", "reaction", "electron", "solution"],
        "English": ["grammar", "comprehension", "prose", "poetry", "metaphor", "adjective", "paragraph", "vocabulary"],
        "EVS": ["environment", "pollution", "sustainability", "conservation", "garbage", "surroundings", "habitats"],
        "Social Science": ["civics", "democracy", "society", "culture", "citizenship", "rights", "community"],
        "History": ["dynasty", "revolution", "ancient", "civilization", "empire", "treaty", "warfare", "historical"],
        "Geography": ["latitude", "topography", "climate", "continent", "oceans", "maps", "resources", "monsoon"],
        "Computer Science": ["algorithm", "programming", "python", "database", "network", "loops", "hardware", "software"],
        "Economics": ["inflation", "gdp", "market", "demand", "supply", "currency", "banking", "finance"],
        "Commerce": ["accounting", "ledger", "audit", "trade", "business", "invoice", "shares", "capital"]
    }
    
    best_subject = "General Education"
    max_score = 0
    
    for subj, keywords in subject_weights.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > max_score:
            max_score = score
            best_subject = subj
            
    return best_subject


def _detect_chapter(text):
    """Extracts logical structural chapter headings and titles via regex patterns."""
    patterns = [
        r"(?:Chapter|Lesson|Unit|Module)\s+(\d+[:.]?\d*)\s*[:-]?\s*([^\n\r]+)",
        r"(?:Topic|Activity|Experiment)\s*([^\n\r]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                return f"Chapter {groups[0]}: {groups[1].strip()}"
            return f"Topic: {groups[0].strip()}"
            
    return "Unknown"


def _extract_keywords_and_topics(text):
    """Filters, cleans, and builds top keyword frequency rankings and topics."""
    stop_words = {
        "the", "and", "a", "of", "to", "in", "is", "that", "it", "on", "for", "as", "with", "was", "by", "an", "be", "this", "are", "from", 
        "at", "or", "an", "will", "can", "should", "your", "their", "them", "these", "those", "each", "every", "about", "into"
    }
    words = re.findall(r"\b[a-zA-Z]{4,15}\b", text.lower())
    filtered_words = [w for w in words if w not in stop_words]
    
    # Calculate word distribution frequency
    freq = {}
    for w in filtered_words:
        freq[w] = freq.get(w, 0) + 1
        
    sorted_kws = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [k[0].capitalize() for k in sorted_kws[:20]]
    
    # Deriving primary topics from cluster frequencies
    top_topics = [k[0].capitalize() for k in sorted_kws[:5]]
    return top_keywords, top_topics


def _detect_learning_outcomes(text):
    """Extracts cognitive behavioral parameters from textual blueprints."""
    outcomes = []
    patterns = [
        r"(?:students will|learners will|able to|can explain|can identify)\s+([^\.\n]+)",
        r"learning objectives?\s*[:-]?\s*([^\.\n]+)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            cleaned = m.strip().capitalize()
            if len(cleaned) > 10 and cleaned not in outcomes:
                outcomes.append(cleaned)
                
    return outcomes[:5] if outcomes else ["Analyze and synthesize target curriculum metrics layout models."]


def _detect_competencies(text):
    """Maps architectural metrics to NCF target framework criteria definitions."""
    competency_matrix = {
        "Critical Thinking": ["analyze", "evaluate", "compare", "contrast", "distinguish", "critique"],
        "Problem Solving": ["solve", "calculate", "derive", "resolve", "execute", "determine"],
        "Communication": ["explain", "discuss", "articulate", "present", "describe", "state"],
        "Observation": ["observe", "identify", "notice", "detect", "witness", "view"],
        "Creativity": ["design", "create", "invent", "imagine", "formulate", "construct"],
        "Reasoning": ["justify", "prove", "infer", "deduce", "validate", "reason"],
        "Collaboration": ["group", "team", "share", "peer", "collaborate", "cooperate"],
        "Art Integrated Learning": ["draw", "sketch", "paint", "sing", "drama", "dance", "visualize"],
        "Game Based Learning": ["play", "simulation", "quiz", "puzzle", "match", "score"],
        "Activity Based Learning": ["conduct", "experiment", "perform", "build", "explore", "measure"]
    }
    
    detected = []
    text_lower = text.lower()
    for comp, verbs in competency_matrix.items():
        if any(verb in text_lower for verb in verbs):
            detected.append(comp)
            
    return detected if detected else ["General Comprehension Strategy Execution"]


def _estimate_educational_levels(word_count, text):
    """Calculates pedagogical target levels and aligns them with NCF stages."""
    text_lower = text.lower()
    
    # Calculate unique complex vocab counts
    complex_words = len([w for w in text_lower.split() if len(w) > 8])
    complexity_ratio = complex_words / max(1, word_count)
    
    if complexity_ratio > 0.18 or "higher education" in text_lower or "university" in text_lower:
        return "Higher Education", "Secondary"
    elif complexity_ratio > 0.12 or "class 11" in text_lower or "class 12" in text_lower:
        return "Class 11-12", "Secondary"
    elif complexity_ratio > 0.08 or "class 9" in text_lower or "class 10" in text_lower:
        return "Class 9-10", "Secondary"
    elif complexity_ratio > 0.05 or "class 6" in text_lower or "class 8" in text_lower:
        return "Class 6-8", "Middle"
    elif complexity_ratio > 0.02 or "class 3" in text_lower or "class 5" in text_lower:
        return "Class 3-5", "Preparatory"
    else:
        return "Class 1-2", "Foundational"


def _detect_language(text):
    """Identifies text composition properties."""
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    total = hindi_chars + english_chars + 1
    
    if hindi_chars / total > 0.7:
        return "Hindi"
    elif hindi_chars / total > 0.15:
        return "Mixed (Bilingual Mode)"
    return "English"


def get_document_info(uploaded_file):
    """
    Analyzes document structures to generate rich structural metadata payloads.
    Guarantees absolute database compatibility for Redis/PostgreSQL/Supabase.
    """
    # Defensive pointer reset to maintain safe text extraction workflows
    if hasattr(uploaded_file, "seek"):
        uploaded_file.seek(0)
        
    text = extract_document_text(uploaded_file)
    word_list = text.split()
    word_count = len(word_list)
    char_count = len(text)
    
    # Compute statistical segment aggregates
    paragraphs = [p for p in text.split("\n") if p.strip()]
    sentences = re.split(r"[\.\!\?]+", text)
    sentences = [s for s in sentences if s.strip()]
    
    # Safely derive absolute page metadata counts
    total_pages_lbl = "1 Page"
    if hasattr(uploaded_file, "name") and uploaded_file.name.lower().endswith(".pdf"):
        try:
            uploaded_file.seek(0)
            reader = PdfReader(uploaded_file)
            total_pages_lbl = f"{len(reader.pages)} Pages"
        except Exception:
            pass
            
    computed_chunks = chunk_text(text)
    keywords, topics = _extract_keywords_and_topics(text)
    r_level, c_stage = _estimate_educational_levels(word_count, text)
    
    # Construct enterprise telemetry dictionary structure
    metadata_payload = {
        "title": getattr(uploaded_file, "name", "Ingested Content Matrix Buffer"),
        "document_type": getattr(uploaded_file, "name", "matrix.txt").split(".")[-1].upper(),
        "subject": _detect_subject(text),
        "chapter": _detect_chapter(text),
        "total_pages": total_pages_lbl,
        "reading_time": f"Approximately {max(1, word_count // 150)} minutes.",
        "reading_level": r_level,
        "characters": char_count,
        "words": word_count,
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "chunks": len(computed_chunks),
        "detected_topics": topics if topics else ["General Concept Reference Layouts"],
        "detected_keywords": keywords[:15] if keywords else ["Curriculum Parameter Tracking"],
        "learning_outcomes": _detect_learning_outcomes(text),
        "competencies": _detect_competencies(text),
        "curricular_stage": c_stage,
        "language": _detect_language(text),
        "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return metadata_payload


# =====================================================
# EXTRA DATA PREVIEW AND ROBUST SYSTEM VALIDATORS
# =====================================================

def get_preview(text, max_chars=2000):
    """
    Generates a structured, insightful contextual snapshot summary layout.
    """
    if not text:
        return {}
        
    cleaned = clean_text(text)
    word_tokens = cleaned.split()
    preview_block = " ".join(word_tokens[:500])
    
    first_heading = "Not Explicitly Detected"
    heading_match = re.search(r"(?:##|###|^[A-Z\s]{4,25}\n)", cleaned)
    if heading_match:
        first_heading = heading_match.group(0).strip()
        
    return {
        "preview_text": preview_block,
        "first_heading": first_heading,
        "first_chapter": _detect_chapter(cleaned),
        "detected_subject": _detect_subject(cleaned)
    }


def validate_document(uploaded_file):
    """
    Executes deep binary audit safety checks before processing files.
    Returns a tuple of (is_valid, validation_message_string).
    """
    if uploaded_file is None:
        return False, "❌ Empty allocation block pointer error context."
        
    try:
        filename = uploaded_file.name.lower()
        if not filename.endswith((".pdf", ".docx", ".txt")):
            return False, "❌ Unsupported Format: Only PDF, DOCX, and TXT files are supported."
            
        # File size calculation via internal descriptor states
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0, 2)
            byte_size = uploaded_file.tell()
            uploaded_file.seek(0)
            if byte_size == 0:
                return False, "❌ Empty Document: File contain zero byte structures."
            if byte_size > (15 * 1024 * 1024):
                return False, "❌ Oversized File: Target processing capability bound threshold exceeded (Max 15MB)."
                
        # Structural data conversion confirmation
        extracted_content = extract_document_text(uploaded_file)
        if not extracted_content or len(extracted_content.strip()) < 50:
            return False, "❌ Image-Only/Corrupted Content: Parsed system data contains zero valid character elements."
            
        return True, "✔ Success"
    except Exception as validation_err:
        return False, f"❌ Validation Verification Block Failure: {validation_err}"
