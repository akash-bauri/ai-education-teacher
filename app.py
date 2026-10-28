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
