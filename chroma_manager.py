import streamlit as st
import faiss
import numpy as np
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_model()


# ==========================================
# STORE DOCUMENT
# ==========================================

def store_document_chunks(
    chunks,
    document_name="document",
    page_numbers=None,
    subject="Unknown",
    chapter="Unknown"
):
    try:
        if not chunks:
            return False

        # Generate enterprise identification and audit markers
        document_id = str(uuid.uuid4())
        uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_chunks = len(chunks)

        embeddings = model.encode(
            chunks,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype(
            np.float32
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            embeddings
        )

        # Generate comprehensive enterprise metadata architecture
        metadata = []
        for i, chunk in enumerate(chunks):
            word_count = len(chunk.split())
            character_count = len(chunk)

            metadata.append({
                "document": document_name,
                "document_id": document_id,
                "document_version": 1,
                "page": (
                    page_numbers[i]
                    if page_numbers and i < len(page_numbers)
                    else "Unknown"
                ),
                "chunk": i + 1,
                "total_chunks": total_chunks,
                "chapter": chapter,
                "subject": subject,
                "uploaded_at": uploaded_at,
                "word_count": word_count,
                "character_count": character_count,
                "embedding_model": "all-MiniLM-L6-v2",
                "embedding_dimension": dimension,
                "embedding": embeddings[i].tolist(),
                "retrieval_method": "FAISS Semantic Search"
            })

        st.session_state["faiss_index"] = index
        st.session_state["document_chunks"] = chunks
        st.session_state["document_metadata"] = metadata
        st.session_state["document_name"] = document_name
        st.session_state["embedding_count"] = total_chunks

        return True

    except Exception as e:
        st.error(f"FAISS Error: {str(e)}")
        return False


# ==========================================
# SEARCH DOCUMENT
# ==========================================

def search_document(
    query,
    top_k=5
):
    try:
        if "faiss_index" not in st.session_state:
            return []

        index = st.session_state["faiss_index"]

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = query_embedding.astype(
            np.float32
        )

        distances, indices = index.search(
            query_embedding,
            top_k
        )

        chunks = st.session_state.get(
            "document_chunks",
            []
        )
        
        # Defensive metadata lookup to prevent state KeyErrors
        session_metadata = st.session_state.get(
            "document_metadata", 
            []
        )

        results = []

        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(chunks):
                distance = distances[0][i]

                if distance < 2.0:
                    similarity = max(0, round(1 - (distance / 2), 2))
                    
                    # Enterprise Confidence Cap: 70% floor, 99% ceiling
                    confidence = min(99, max(70, round(similarity * 100)))
                    
                    # Calculate system evaluation score
                    retrieval_score = round(1 / (1 + distance), 4)
                    
                    # Safe fallback block configuration
                    if idx < len(session_metadata):
                        chunk_metadata = session_metadata[idx]
                    else:
                        chunk_metadata = {
                            "document": "Unknown",
                            "document_id": "Unknown",
                            "document_version": 1,
                            "page": "Unknown",
                            "chunk": i + 1,
                            "total_chunks": len(chunks),
                            "chapter": "Unknown",
                            "subject": "Unknown",
                            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "word_count": len(chunks[idx].split()),
                            "character_count": len(chunks[idx]),
                            "embedding_model": "all-MiniLM-L6-v2",
                            "embedding_dimension": 384,
                            "embedding": [],
                            "retrieval_method": "FAISS Semantic Search"
                        }

                    results.append({
                        "text": chunks[idx],
                        "distance": float(distance),
                        "similarity": similarity,
                        "confidence": confidence,
                        "retrieval_score": retrieval_score,
                        "rank": i + 1,
                        "retrieved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "metadata": chunk_metadata
                    })

        # Deterministic quality sorting: sort descending by similarity, then retrieval_score
        results.sort(
            key=lambda x: (x["similarity"], x["retrieval_score"]),
            reverse=True
        )

        return results

    except Exception:
        return []


# ==========================================
# GET CONTEXT
# ==========================================

def get_context(
    query,
    top_k=5
):
    results = search_document(
        query,
        top_k
    )

    if not results:
        return ""

    return "\n\n".join(
        item["text"]
        for item in results
    )


# ==========================================
# GET SOURCE INFORMATION
# ==========================================

def get_source_information(
    query,
    top_k=1
):
    results = search_document(
        query,
        top_k
    )

    if not results:
        return None

    item = results[0]

    return {
        "document": item["metadata"]["document"],
        "document_id": item["metadata"]["document_id"],
        "document_version": item["metadata"]["document_version"],
        "page": item["metadata"]["page"],
        "chunk": item["metadata"]["chunk"],
        "total_chunks": item["metadata"]["total_chunks"],
        "chapter": item["metadata"]["chapter"],
        "subject": item["metadata"]["subject"],
        "similarity": item["similarity"],
        "confidence": item["confidence"],
        "retrieval_score": item["retrieval_score"],
        "rank": item["rank"],
        "retrieved_at": item["retrieved_at"],
        "uploaded_at": item["metadata"]["uploaded_at"],
        "word_count": item["metadata"]["word_count"],
        "character_count": item["metadata"]["character_count"],
        "embedding_model": item["metadata"]["embedding_model"],
        "embedding_dimension": item["metadata"]["embedding_dimension"],
        "retrieval_method": item["metadata"]["retrieval_method"]
    }


# ==========================================
# DOCUMENT COUNT
# ==========================================

def get_document_count():
    return len(
        st.session_state.get(
            "document_chunks",
            []
        )
    )


# ==========================================
# DOCUMENT NAME
# ==========================================

def get_document_name():
    return st.session_state.get(
        "document_name",
        "No Document"
    )


# ==========================================
# EMBEDDING COUNT
# ==========================================

def get_embedding_count():
    return st.session_state.get(
        "embedding_count",
        0
    )


# ==========================================
# CLEAR DOCUMENTS
# ==========================================

def clear_documents():
    keys = [
        "faiss_index",
        "document_chunks",
        "document_metadata",
        "document_name",
        "embedding_count"
    ]

    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

    return True
