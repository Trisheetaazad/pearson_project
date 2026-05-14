def extract_case_fields(text):
    case_no_pattern = r"Case No[:\s]+([A-Z0-9\-]+)"
    date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    
    case_no = re.search(case_no_pattern, text)
    date_found = re.search(date_pattern, text)
    
    return {
        "case_id": case_no.group(1) if case_no else "Unknown", 
        "filing_date": date_found.group(1) if date_found else "Unknown"
    }