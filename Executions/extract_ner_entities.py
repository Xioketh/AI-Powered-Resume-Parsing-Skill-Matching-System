from transformers import pipeline
import re


ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def filter_organizations(orgs):
    common_false_positives = {
        "Spring", "Boot", "Angular", "MongoDB", "React", "Docker", "Java", "Python", "JWT", "Android","MySQL","Node Express","Express js"
    }
    return [org for org in orgs if org not in common_false_positives and len(org) > 2]

def extract_ner_entities(text):
    text = text.replace("\n", " ").replace("  ", " ")
    results = ner_pipeline(text)

    # Group entities
    names = [r["word"] for r in results if r["entity_group"] == "PER"]
    orgs = [r["word"] for r in results if r["entity_group"] == "ORG"]
    dates = [r["word"] for r in results if r["entity_group"] == "DATE"]

    # Use regex for better accuracy on known fields
    name_regex = re.search(r"^(.*?)\s+(Associate|Software|Engineer|Undergraduate)", text)
    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.search(r"\+?\d[\d\s\-]{9,}", text)
    date_ranges = re.findall(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4}", text)

    orgs = filter_organizations(orgs);
    return {
        "name": name_regex.group(1).strip() if name_regex else (names[0] if names else None),
        "email": email.group(0) if email else None,
        "phone": phone.group(0).strip() if phone else None,
        # "organizations": list(set(orgs)),
        # "dates": list(set(dates + date_ranges))
    }