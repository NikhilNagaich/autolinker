import openai
import os
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")

EMBED_MODEL = "text-embedding-3-small"

def get_embedding(text: str) -> List[float]:
    text = text.replace("\n", " ")
    response = openai.embeddings.create(
        input=[text],
        model=EMBED_MODEL
    )
    return response.data[0].embedding

def embed_blog(blog):
    full_text = blog["title"] + "\n\n" + blog["content"]
    blog_vector = get_embedding(full_text)

    sentence_vectors = []
    for sentence in blog["sentences"]:
        vec = get_embedding(sentence)
        sentence_vectors.append(vec)

    return {
        **blog,
        "blog_vector": blog_vector,
        "sentence_vectors": sentence_vectors
    }
