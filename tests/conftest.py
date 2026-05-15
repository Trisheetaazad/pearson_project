import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Check if already in sys.path to avoid duplicates
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from app.ocr.engine import process_document
    print("✅ Project modules loaded successfully.")
except ImportError as e:
    print(f"❌ Failed to load modules. Check your path: {ROOT}")
    print(e)

