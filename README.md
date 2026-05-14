# Pearson Project: Legal Case Fact Summary ⚖️

Pearson AI is a document processing pipeline designed to convert messy legal scans and PDF documents into clean, structured summaries. By combining **Tesseract OCR**, **Llama 3.3 (via Groq)**, and **RAG-based retrieval**, this tool provides a side-by-side verification interface and a continuous human-in-the-loop learning system.

---

## 🛠️ Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **OCR Engine:** [Tesseract](https://github.com/tesseract-ocr/tesseract) & [PyMuPDF](https://pymupdf.readthedocs.io/)
- **LLM Reasoning:** [Groq](https://groq.com/) (Llama 3.3 70B) & [Gemini 1.5 Flash](https://aistudio.google.com/)
- **Vector Search:** [FAISS](https://github.com/facebookresearch/faiss) & [Sentence-Transformers](https://www.sbert.net/)

---

## 📁 Repository Structure
```text
pearson_project/
├── app/
│   ├── api/
│        └── main.py            # Streamlit UI logic (main.py)
│   ├── drafting/
│        └── geberator.py       # LLM Summary Generation (generator.py)
│   ├── extraction
│        └── parser.py          # Data harvesting (parser.py)        
│   ├── learning/ 
│        └── feedback.py        # Feedback loop & JSONL management (feedback.py)
│   ├── ocr/ 
│        └── engine.py          # OCR & Text Reconstruction (engine.py)
│   └── retrieval/
│        └──  vectordb.py       # Vector database & RAG (vectordb.py)
├── data/                       # Storage for inputs, extractions, summaries
│   ├── extracted
│   ├── feedback
│   ├── inputs
│   └── summaries
├── tests/                      # Unit tests for core processing
└── requirements.txt            # Python dependencies



⚙️ Setup & Instructions

1. System Requirements
Install the Tesseract OCR engine on your Linux machine:

Bash
sudo apt update && sudo apt install tesseract-ocr -y

2. Execution
To launch the application, run the following command in your terminal:

Bash
python3 -m streamlit run app/api/main.py