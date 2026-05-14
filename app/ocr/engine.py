import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

def clean_text_with_groq(raw_text):
    """
    Uses Llama 3.3 to reconstruct and clean noisy legal OCR text.
    Processes text page-by-page to ensure no data is lost.
    """
    if not raw_text.strip() or len(raw_text) < 10:
        return raw_text

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # System Prompt tuned for pattern recognition and legal reconstruction
    system_msg = (
        "You are a Legal Document Restoration Expert. Your task is to take messy OCR text and "
        "reconstruct it into a clean, professional legal format. \n\n"
        "RULES:\n"
        "1. Fix obvious OCR typos (e.g., 'tiny' -> 'day', 'betemen' -> 'between'). You can change spellings.\n"
        "2. Remove unnecessary large spaces, line breaks in the middle of sentences, and random symbols.\n"
        "3. Preserve all specific data like Names, Addresses, Dates, and Amounts exactly.\n"
        "4. Standardize the headers (e.g., PREMISES, TERM, RENT, ARTICLE).\n"
        "5. Return ONLY the reconstructed text without any preamble.\n"
        "6. If a line does not make sense, try to infer the most likely intended text based on context, "
        "while trying to keep the structure and meaning same but do not add any new information."
    )
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Reconstruct this legal text section:\n\n{raw_text}"}
            ],
            temperature=0.0 
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq Cleaning Error: {e}")
        return raw_text

def process_document(file_path):
    """
    Analyzes the document page-by-page. 
    Handles hybrid PDFs containing both images (scans) and digital text.
    """
    ext = file_path.lower().split('.')[-1]
    final_reconstructed_text = ""
    
    if ext == 'pdf':
        doc = fitz.open(file_path)
        
        for page_num, page in enumerate(doc):
            # 1. Attempt to extract digital text 
            page_raw_text = page.get_text().strip()
            
            # 2. If no text found, use OCR 
            if not page_raw_text:
                # Use a Matrix to zoom in (2x) for higher OCR accuracy
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_raw_text = pytesseract.image_to_string(img)
            
            # 3. Clean and Reconstruct each page individually
            if page_raw_text:
                cleaned_page = clean_text_with_groq(page_raw_text)
                # Append with page markers for clarity in the UI
                final_reconstructed_text += f"\n--- PAGE {page_num + 1} ---\n{cleaned_page}\n"
        
        doc.close()
        return final_reconstructed_text

    # Handling for direct image uploads (JPG/PNG)
    elif ext in ['jpg', 'jpeg', 'png']:
        raw_image_text = pytesseract.image_to_string(Image.open(file_path))
        return clean_text_with_groq(raw_image_text)
    
    else:
        return "Unsupported file format."