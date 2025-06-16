import nltk
from typing import List

def clean_text(text: str) -> List[str]:
    # Basic sentence splitting
    sentences = nltk.sent_tokenize(text)

    # Clean each sentence
    clean_sentences = []
    for s in sentences:
        s = s.strip().replace("\n", " ")
        if 20 < len(s) < 500:  # Skip very short or too long junk
            clean_sentences.append(s)

    return clean_sentences
