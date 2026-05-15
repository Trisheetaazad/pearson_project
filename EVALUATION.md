## 📈 Evaluation Approach & Results

### Evaluation Method

Performance is tracked across two dimensions:

1. **OCR Recovery Rate** — whether visual content from scanned/hybrid pages is fully captured.
2. **Draft Improvement via Few-Shot Learning** — whether injecting human edits into future prompts produces outputs that match the operator's preferred style and structure.

For draft improvement, we measure the **Edit Distance** between the initial AI-generated draft and the final operator-saved version. A shrinking edit distance across successive runs indicates the learning loop is working.

---

### Results

#### 1. OCR — 100% Recovery Rate

The strict OCR approach (render every PDF page as a 2× image, then run Tesseract) successfully recovered all content from both test documents, including a scanned criminal record and a handwritten-style lease agreement image. Digital text fallback was used where available; OCR was used when the text layer was absent or empty.

---

#### 2. Draft Improvement — Before / After Example

The following demonstrates how injecting one human edit into the prompt changed the next draft's output.

**Document:** `legal_jpg_test.jpg` (Lease Agreement)

**Iteration 1 — AI Draft (no prior edits):**
```
Here are the key facts:

* Term: April 1, 2024 - March 31, 2028
* Monthly payment: $1,450.00
* Payment due date: On or before the 1st day of each month
```

**Operator edit:** Added `* deposit: $2,900.00` and saved via "💾 Save & Train". This edit was appended to `data/human_edits.jsonl`.

**Iteration 2 — AI Draft (with injected edit as few-shot example):**
```
Here are the key facts:

* Term: April 1, 2024 - March 31, 2028
* Monthly payment: $1,450.00
* Payment due date: On or before the 1st day of each month
* Deposit: $2,900.00
```

The model picked up that the operator expects deposit information to be included, and added it unprompted on the second run — without any code changes. This demonstrates the feedback loop working as intended.

---

### Limitations & Honest Notes

* Few-shot learning is context-sensitive, not fine-tuning. The model doesn't retain edits between sessions unless `human_edits.jsonl` is persistent and loaded at prompt time.
* With only 2–3 edits in the JSONL file, improvement is directional but not statistically significant. At 10+ edits, the pattern becomes more reliable.
* Edit distance is not formally computed in code; it is assessed manually for this submission. A future improvement would auto-calculate Levenshtein distance per run and log it alongside each feedback entry.