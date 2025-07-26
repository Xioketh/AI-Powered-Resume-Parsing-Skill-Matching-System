import re


def extract_about(text):
    # Match "About Me" or "ABOUT ME" or similar, optionally followed by colon or spaces
    # Capture everything until the next all uppercase heading (2+ uppercase letters with spaces)
    pattern = re.compile(
        r"(ABOUT ME|About Me|Profile|Summary)[:\s]*\n?(.*?)(?=\n[A-Z\s]{2,}\n|$)",
        re.DOTALL | re.IGNORECASE
    )

    match = pattern.search(text)
    if match:
        about_text = match.group(2).strip()
        # Optional: Replace multiple newlines with a single newline for neatness
        about_text = re.sub(r'\n+', '\n', about_text)
        return about_text
    return None
