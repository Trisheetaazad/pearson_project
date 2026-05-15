# Pearson Project: Legal Case Fact Summary ⚖️

Pearson AI is a document processing pipeline designed to convert messy legal scans and PDF documents into clean, structured summaries. By combining **Tesseract OCR**, **Llama 3.3 (via Groq)**, and **RAG-based retrieval**, this tool provides a side-by-side verification interface and a continuous human-in-the-loop learning system.

---

## 🛠️ Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **OCR Engine:** [Tesseract](https://github.com/tesseract-ocr/tesseract) & [PyMuPDF](https://pymupdf.readthedocs.io/)
- **LLM Reasoning:** [Groq](https://groq.com/) (Llama 3.3 70B) & [Gemini 1.5 Flash](https://aistudio.google.com/)
- **Vector Search:** [FAISS](https://github.com/facebookresearch/faiss) & [Sentence-Transformers](https://www.sbert.net/)

---

```text
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
├── data/                     # Persistent storage
│   ├── extracted/
│   ├── feedback/
│   ├── inputs/
│   └── summaries/
├── tests/                    # Unit tests for core processing
├── requirements.txt          # Python library dependencies
└── packages.txt              # System-level dependencies (tesseract-ocr)



⚙️ Setup & Instructions
1. Local Environment Setup
Run these commands in your terminal to prepare your local Linux environment:

```bash
# Install the Tesseract OCR engine
sudo apt update && sudo apt install tesseract-ocr -y

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up your API keys
cp .env.example .env
# Then open .env and fill in your GROQ_API_KEY and GEMINI_API_KEY
2. Execution
To launch the application locally, use the following command:

```bash
python3 -m streamlit run app/api/main.py
3. GitHub & Streamlit Cloud Deployment
To deploy this project from GitHub to Streamlit Cloud, ensure your repository contains the following configuration files in the root directory:

requirements.txt: Contains all Python libraries.

packages.txt: Contains exactly one line: tesseract-ocr.

.gitignore: Should include .env, __pycache__/, and data/ to keep your repo clean and secure.

Streamlit Cloud Path:
When deploying, set the Main file path to:

app/api/main.py