import re


def extract_case_fields(text):
    """
    Extracts structured metadata fields from cleaned legal document text.
    Returns a dictionary of key fields for downstream use.
    """
    case_no_pattern  = r"Case No[:\s]+([A-Z0-9\-]+)"
    date_pattern     = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    party_pattern    = r"(?:Plaintiff|Defendant|Petitioner|Respondent)[:\s]+([A-Z][a-zA-Z\s,\.]+)"
    amount_pattern   = r"\$[\d,]+(?:\.\d{2})?"
    doc_type_pattern = r"\b(Lease Agreement|Criminal Record|Last Will|Affidavit|Complaint|Indictment|Motion|Order|Judgment)\b"

    case_no    = re.search(case_no_pattern, text)
    date_found = re.search(date_pattern, text)
    party      = re.search(party_pattern, text)
    amounts    = re.findall(amount_pattern, text)
    doc_type   = re.search(doc_type_pattern, text, re.IGNORECASE)

    return {
        "case_id":     case_no.group(1)        if case_no    else "Unknown",
        "filing_date": date_found.group(1)     if date_found else "Unknown",
        "party":       party.group(1).strip()  if party      else "Unknown",
        "amounts":     amounts                 if amounts    else [],
        "doc_type":    doc_type.group(1)       if doc_type   else "Unknown",
    }