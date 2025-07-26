import os

from Executions.extract_ner_entities import extract_ner_entities
from Executions.extract_about import extract_about
from Executions.extract_skills import extract_skills
from Executions.ocr_from_scanned_pdf import ocr_from_scanned_pdf


def parse_scanned_cv(pdf_path, required_skills=None):
    if not os.path.exists(pdf_path):
        print("❌ File not found.")
        return {}

    text = ocr_from_scanned_pdf(pdf_path)
    if not text.strip():
        print("❌ No text found in the PDF (is it blank or not a scanned CV?).")
        return {}

    preprocess_text = preprocess_text_for_ner(text)

    entities = extract_ner_entities(preprocess_text)
    skills = extract_skills(preprocess_text)
    about = extract_about(text)

    match_result = calculate_skill_match(skills["skills"], required_skills)

    return {
        "name": entities["name"],
        "email": entities["email"],
        "phone": entities["phone"],
        "skills": skills["skills"],
        "skillsAverageConfidence": skills["average_confidence"],
        "about": about,
        "matchedSkills": match_result["matched"],
        "matchPercentage": match_result["percentage"]
    }


def preprocess_text_for_ner(text: str) -> str:
    text = text.replace("\n", " ").replace("  ", " ")
    return text


def calculate_skill_match(extracted_skills, required_skills):
    if not required_skills:
        return {"matched": [], "percentage": 0.0}

    extracted = [s.lower().strip() for s in extracted_skills]
    required = [s.lower().strip() for s in required_skills]

    matched = [skill for skill in required if skill in extracted]
    percentage = (len(matched) / len(required)) * 100 if required else 0.0

    return {"matched": matched, "percentage": round(percentage, 2)}


if __name__ == "__main__":
    file_path = "sample_cv.pdf"
    input_skills = input("Enter required skills (comma separated): ").split(",")



    result = parse_scanned_cv(file_path, input_skills)

    for key, value in result.items():
        print(f"{key}: {value}")

