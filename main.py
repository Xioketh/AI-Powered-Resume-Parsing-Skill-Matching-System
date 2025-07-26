import pdfplumber
import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# ---- 1. Extract text from PDF ----
def extract_text_from_pdf(file_path):
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text

# ---- 2. Use regex to extract email and phone ----
def extract_email_and_phone(text):
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"(\+?\d{1,3})?\s?\(?\d{2,4}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}", text)
    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
    }

# ---- 3. Use spaCy to extract name, organizations, and dates ----
def extract_entities(text):
    doc = nlp(text)
    entities = {
        "name": None,
        "organizations": [],
        "dates": []
    }

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["name"]:
            entities["name"] = ent.text
        elif ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)

    return entities

# ---- 4. Run Everything ----
def parse_cv(file_path):
    text = extract_text_from_pdf(file_path)
    contact_info = extract_email_and_phone(text)
    entities = extract_entities(text)

    return {
        "name": entities["name"],
        "email": contact_info["email"],
        "phone": contact_info["phone"],
        "organizations": list(set(entities["organizations"])),
        "dates": list(set(entities["dates"]))
    }

# ---- 5. Test ----
if __name__ == "__main__":
    file_path = "sample_cv.pdf"
    # file_path = "sample_cv2.pdf"
    # file_path = "sample_cv3.pdf"
    # file_path = "sample_cv4.pdf"
    result = parse_cv(file_path)
    print(result)