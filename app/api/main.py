import streamlit as st
import os
import json
from datetime import datetime
from app.ocr.engine import process_document
from app.retrieval.vectordb import create_index, query_index
from app.drafting.generator import generate_summary
from app.learning.feedback import save_feedback

# 1. Page Configuration
st.set_page_config(page_title="Pearson AI", layout="wide")
st.title("⚖️ Case Fact Summary")

# 2. Initialize Session State
# We now store results in a dictionary: {filename: {"extracted": "", "summary": ""}}
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

# 3. Sidebar Navigation
st.sidebar.header("Navigation")

if st.sidebar.button("Start New Session"):
    st.session_state.results = {}
    st.session_state.uploader_key += 1
    st.rerun()

st.sidebar.divider()
st.sidebar.header("Model Settings")
provider_choice = st.sidebar.radio("Select Provider", ["Gemini", "Groq"])

# 4. Multi-File Upload
# accept_multiple_files=True allows users to drop a batch of files
uploaded_files = st.file_uploader(
    "Upload Case Documents", 
    type=["pdf", "png", "jpg"], 
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

# 5. Process All Files Button
if uploaded_files:
    # Folders setup
    folders = ["data/inputs", "data/extracted", "data/summaries", "data/feedback"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Only show "Process" if there are files uploaded that aren't in results yet
    files_to_process = [f for f in uploaded_files if f.name not in st.session_state.results]
    
    if files_to_process:
        if st.button(f"🚀 Process {len(files_to_process)} New Files"):
            for uploaded_file in files_to_process:
                with st.status(f"Processing {uploaded_file.name}...", expanded=True) as status:
                    try:
                        # Save input
                        input_path = os.path.join("data/inputs", uploaded_file.name)
                        with open(input_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # OCR & Reconstruction
                        st.write("🔍 Running OCR and Cleaning...")
                        cleaned_text = process_document(input_path)
                        
                        # Save extracted text
                        base_name = os.path.splitext(uploaded_file.name)[0]
                        with open(os.path.join("data/extracted", f"{base_name}.txt"), "w") as f:
                            f.write(cleaned_text)
                        
                        # Retrieval & Summary
                        st.write("📝 Drafting Summary")
                        chunks = [c for c in cleaned_text.split('\n\n') if len(c) > 40]
                        index, _ = create_index(chunks)
                        context_chunks = query_index("Summary of core facts", index, chunks)
                        
                        summary = generate_summary(
                            " ".join(context_chunks), 
                            "Summarize the key facts concisely.", 
                            provider=provider_choice.lower()
                        )
                        
                        # Store in session state
                        st.session_state.results[uploaded_file.name] = {
                            "extracted": cleaned_text,
                            "summary": summary
                        }
                        
                        # Save initial summary file
                        with open(os.path.join("data/summaries", f"{base_name}.txt"), "w") as f:
                            f.write(summary)
                            
                        status.update(label=f"✅ {uploaded_file.name} Complete!", state="complete")
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
            st.rerun()

# 6. Display Results Individually
if st.session_state.results:
    st.divider()
    st.header("📂 Processed Results")
    
    # Create an expander or tab for each file to keep the UI clean
    for filename, data in st.session_state.results.items():
        with st.expander(f"📄 {filename}", expanded=False):
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("### 🔍 Cleaned Source")
                # Individual text area for specific file extraction
                st.text_area(
                    "Source Content", 
                    value=data["extracted"], 
                    height=400, 
                    key=f"src_{filename}"
                )

            with col_right:
                st.markdown("### 📝 Drafted Summary")
                # Individual editable summary for specific file
                edited_summary = st.text_area(
                    "Edit Summary", 
                    value=data["summary"], 
                    height=400, 
                    key=f"sum_{filename}"
                )
                
                if st.button("💾 Save & Train", key=f"btn_{filename}"):
                    base_name = os.path.splitext(filename)[0]
                    
                    # Update summary text file
                    with open(os.path.join("data/summaries", f"{base_name}.txt"), "w") as f:
                        f.write(edited_summary)
                    
                    # Save feedback JSON
                    feedback_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "filename": filename,
                        "original_ai_draft": data["summary"],
                        "human_final_edit": edited_summary
                    }
                    feedback_path = os.path.join("data/feedback", f"{base_name}_feedback.json")
                    with open(feedback_path, "w") as f:
                        json.dump(feedback_entry, f, indent=4)
                    
                    save_feedback(data["summary"], edited_summary, filename)
                    st.success(f"Saved {filename}!")