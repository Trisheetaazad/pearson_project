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
pearson_project/
├── app/
│   ├── __init__.py           # Makes 'app' a package
│   ├── api/
│   │    ├── __init__.py      # Makes 'api' a package
│   │    └── main.py          # Streamlit UI logic
│   ├── drafting/
│   │    ├── __init__.py      # Makes 'drafting' a package
│   │    └── generator.py     # LLM Summary Generation
│   ├── extraction/
│   │    ├── __init__.py      # Makes 'extraction' a package
│   │    └── parser.py        # Data harvesting (Regex logic)
│   ├── learning/ 
│   │    ├── __init__.py      # Makes 'learning' a package
│   │    └── feedback.py      # Feedback loop & JSONL management
│   ├── ocr/ 
│   │    ├── __init__.py      # Makes 'ocr' a package
│   │    └── engine.py        # Strict OCR & Text Reconstruction
│   └── retrieval/
│        ├── __init__.py      # Makes 'retrieval' a package
│        └──  vectordb.py     # Vector database & FAISS RAG
├── data/                     # Persistent storage (Git-ignored)
│   ├── extracted/
│   ├── feedback/
│   ├── inputs/
│   └── summaries/
├── tests/                    # Unit tests for core processing
├── requirements.txt          # Python library dependencies
└── packages.txt              # System-level dependencies (tesseract-ocr)



⚙️ Setup & Instructions

1. System Requirements
Install the Tesseract OCR engine on your Linux machine:

Bash
sudo apt update && sudo apt install tesseract-ocr -y

2. Execution
To launch the application, run the following command in your terminal:

Bash
python3 -m streamlit run app/api/main.py