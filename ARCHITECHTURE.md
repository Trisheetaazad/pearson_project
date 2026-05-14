# 🏛️ Architecture Overview: Pearson AI

This document provides a detailed technical breakdown of the modular pipeline used in the Legal Multi-Case Summary Workflow.

## 🔄 The Pipeline Flow
The system is designed as a logic-driven sequence for business process improvement:

### 1. Ingestion & Strict OCR
To ensure 100% content recovery from hybrid PDFs, every page is rendered as a high-resolution image ($2\times$ zoom matrix). These images are processed via **Tesseract OCR**, capturing even faint scans or stamps that digital text layers might miss.

### 2. Restoration (Cleaning)
The raw OCR output is sent to **Llama 3.3 (via Groq)** page-by-page. The model uses contextual pattern recognition to fix common OCR noise (e.g., "tiny" to "day") and reconstruct the document’s original legal structure.

### 3. Metadata Extraction
The `app/utils/extraction.py` utility uses **Regular Expressions (Regex)** to harvest high-value structured data. It specifically targets:
* **Case IDs**: Unique identifiers for tracking.
* **Filing Dates**: Chronological markers for the legal record.

### 4. Vector Store (RAG)
Reconstructed text is split into semantic chunks and embedded using the **SentenceTransformers (`all-MiniLM-L6-v2`)** model. These embeddings are indexed in a **FAISS** vector database to enable precise fact-retrieval during the drafting stage.

### 5. Drafting & Learning Loop
**Gemini 1.5 Flash** or **Llama 3.3** generates the final summaries. This stage utilizes **Few-Shot Learning**, injecting the three most recent human edits from `data/human_edits.jsonl` into the prompt to automatically mimic the user's preferred style and formatting. 