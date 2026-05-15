"""
Unit tests for the OCR engine and downstream modules.
Run with: pytest tests/
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from app.ocr.engine import clean_text_with_groq, process_document
from app.extraction.parser import extract_case_fields
from app.retrieval.vectordb import create_index, query_index
from app.learning.feedback import save_feedback, get_learning_examples


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_LEGAL_TEXT = """
Case No: CR-2019-004472
Date: 11/03/2019
Defendant: John Doe
Charges: Aggravated Assault, Resisting Arrest
Arresting Officer: Ofc. T. Broderick
Amount Owed: $2,500.00
"""

NOISY_OCR_TEXT = "C4se N0: CR-2O19-OO4472 D3fendant: J0hn D0e Charg3s: Agg assault"


# ---------------------------------------------------------------------------
# parser.py
# ---------------------------------------------------------------------------

class TestExtractCaseFields:
    def test_extracts_case_id(self):
        result = extract_case_fields(SAMPLE_LEGAL_TEXT)
        assert result["case_id"] == "CR-2019-004472"

    def test_extracts_filing_date(self):
        result = extract_case_fields(SAMPLE_LEGAL_TEXT)
        assert result["filing_date"] == "11/03/2019"

    def test_extracts_amounts(self):
        result = extract_case_fields(SAMPLE_LEGAL_TEXT)
        assert "$2,500.00" in result["amounts"]

    def test_unknown_when_missing(self):
        result = extract_case_fields("No structured data here.")
        assert result["case_id"] == "Unknown"
        assert result["filing_date"] == "Unknown"
        assert result["amounts"] == []


# ---------------------------------------------------------------------------
# vectordb.py
# ---------------------------------------------------------------------------

class TestVectorDB:
    def test_create_index_returns_index_and_embeddings(self):
        chunks = ["The defendant was arrested.", "The court ruled in favour.", "Bail was set at $500."]
        index, embeddings = create_index(chunks)
        assert embeddings.shape[0] == 3

    def test_query_returns_correct_number_of_results(self):
        chunks = ["Lease term begins April 1.", "Monthly rent is $1,450.", "Security deposit is $2,900."]
        index, _ = create_index(chunks)
        results = query_index("What is the rent?", index, chunks, k=2)
        assert len(results) == 2

    def test_query_k_capped_at_chunk_count(self):
        chunks = ["Only one chunk here."]
        index, _ = create_index(chunks)
        results = query_index("anything", index, chunks, k=5)
        assert len(results) == 1

    def test_most_relevant_chunk_is_returned(self):
        chunks = [
            "The sky is blue and clouds are white.",
            "Monthly rent payment is $1,450 due on the 1st.",
            "The defendant pleaded not guilty.",
        ]
        index, _ = create_index(chunks)
        results = query_index("How much is the rent?", index, chunks, k=1)
        assert "1,450" in results[0]


# ---------------------------------------------------------------------------
# ocr/engine.py — unit-test clean_text_with_groq with a mocked Groq client
# ---------------------------------------------------------------------------

class TestCleanTextWithGroq:
    def test_returns_original_on_empty_input(self):
        result = clean_text_with_groq("   ")
        assert result.strip() == ""

    def test_returns_original_on_short_input(self):
        result = clean_text_with_groq("Hi")
        assert result == "Hi"

    @patch("app.ocr.engine.Groq")
    def test_calls_groq_and_returns_cleaned_text(self, MockGroq):
        mock_client = MagicMock()
        MockGroq.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = (
            "Case No: CR-2019-004472 Defendant: John Doe"
        )

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key", "GROQ_MODEL": "llama-3.3-70b-versatile"}):
            result = clean_text_with_groq(NOISY_OCR_TEXT)

        assert "CR-2019-004472" in result

    @patch("app.ocr.engine.Groq")
    def test_falls_back_to_raw_text_on_groq_error(self, MockGroq):
        mock_client = MagicMock()
        MockGroq.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API error")

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-key", "GROQ_MODEL": "llama-3.3-70b-versatile"}):
            result = clean_text_with_groq(NOISY_OCR_TEXT)

        assert result == NOISY_OCR_TEXT


# ---------------------------------------------------------------------------
# learning/feedback.py
# ---------------------------------------------------------------------------

class TestFeedback:
    def test_save_and_retrieve_feedback(self, tmp_path, monkeypatch):
        feedback_file = tmp_path / "human_edits.jsonl"
        monkeypatch.setattr("app.learning.feedback.FEEDBACK_FILE", str(feedback_file))

        save_feedback("AI draft text", "Human edited text", "test-case-001")
        result = get_learning_examples(limit=1)

        assert "AI draft text" in result
        assert "Human edited text" in result

    def test_get_examples_returns_message_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("app.learning.feedback.FEEDBACK_FILE", str(tmp_path / "nonexistent.jsonl"))
        result = get_learning_examples()
        assert "No previous examples" in result

    def test_get_examples_respects_limit(self, tmp_path, monkeypatch):
        feedback_file = tmp_path / "human_edits.jsonl"
        monkeypatch.setattr("app.learning.feedback.FEEDBACK_FILE", str(feedback_file))

        for i in range(5):
            save_feedback(f"Draft {i}", f"Edit {i}", f"case-{i}")

        result = get_learning_examples(limit=2)
        # Should contain the last 2 edits, not all 5
        assert "Edit 3" in result
        assert "Edit 4" in result
        assert "Edit 0" not in result