from db.supabase_client import get_supabase
import json

def to_pgvector(vector):
    return "[" + ", ".join(f"{v:.6f}" for v in vector) + "]"

def insert_blogs(blogs):
    supabase = get_supabase()
    payload = []

    for blog in blogs:
        payload.append({
            "url": blog["url"],
            "title": blog["title"],
            "slug": blog["slug"],
            "content": blog["content"],
            "content_html": blog["content_html"],  # new field
            "embedding": blog["embedding"],
            "seed_url": blog.get("seed_url", ""),
            "sentences": json.dumps(blog["sentences"])  # or just blog["sentences"] if your client handles it
        })

    result = supabase.table("blogs").upsert(payload).execute()
    print(f"✅ Uploaded {len(result.data)} blogs to Supabase.")
