import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compute_blog_similarities(blogs, top_n=3):
    titles = [b["title"] for b in blogs]
    vectors = np.array([b["blog_vector"] for b in blogs])
    sim_matrix = cosine_similarity(vectors)

    results = []
    for i, row in enumerate(sim_matrix):
        ranked = np.argsort(row)[::-1]  # descending
        top_matches = []
        seen_slugs = set()  # Track slugs already added

        for j in ranked:
            if i == j:
                continue  # skip self
            # Also skip if title and slug are identical (likely duplicate)
            if titles[i] == titles[j] and blogs[i]["slug"] == blogs[j]["slug"]:
                continue
            # Skip if this slug is already added
            if blogs[j]["slug"] in seen_slugs:
                continue
            score = row[j]
            top_matches.append({
                "target_index": j,
                "score": float(score),
                "target_title": titles[j],
                "target_slug": blogs[j]["slug"]
            })
            seen_slugs.add(blogs[j]["slug"])
            if len(top_matches) >= top_n:
                break

        results.append({
            "source_index": i,
            "source_title": titles[i],
            "matches": top_matches
        })

    return results
