from sentence_transformers import SentenceTransformer, util
import re

# Load model and encode skills
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

known_skills = [
    "Python", "Java", "C++", "C#", "JavaScript", "React", "Node.js", "Angular",
    "Django", "Flask", "Spring", "SQL", "MongoDB", "PostgreSQL",
    "Machine Learning", "Deep Learning", "Docker", "Kubernetes",
    "AWS", "GCP", "Azure", "TensorFlow", "PyTorch", "Spring Boot"
]

skill_embeddings = sentence_model.encode(known_skills, convert_to_tensor=True)

def extract_skills(text: str, threshold: float = 0.75):
    skill_confidence = {}

    # Split the resume text into short sentences or phrases
    lines = re.split(r'[.|,\n]', text)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 1. Regex match (high confidence, manually assigned)
        for skill in known_skills:
            if re.search(rf'\b{re.escape(skill)}\b', line, re.IGNORECASE):
                skill_confidence[skill] = max(skill_confidence.get(skill, 0), 0.95)

        # 2. Semantic match (actual cosine similarity)
        line_embedding = sentence_model.encode(line, convert_to_tensor=True)
        cosine_scores = util.cos_sim(line_embedding, skill_embeddings)[0]

        for idx, score in enumerate(cosine_scores):
            score_val = score.item()
            if score_val > threshold:
                skill = known_skills[idx]
                skill_confidence[skill] = max(skill_confidence.get(skill, 0), score_val)

    # Final skill list and average confidence
    if skill_confidence:
        avg_confidence = sum(skill_confidence.values()) / len(skill_confidence)
    else:
        avg_confidence = 0.0

    return {
        "skills": sorted(skill_confidence.keys()),
        "average_confidence": round(avg_confidence, 4)
    }
