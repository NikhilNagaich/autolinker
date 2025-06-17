def run_autolinker_pipeline(input_url):
    # Add these imports at the top if not present
    from input.crawl_urls import crawl_blog_urls
    from input.extract_content import extract_blog_data
    from input.preprocess import clean_text
    from embeddings.generate_embeddings import embed_blog, get_embedding
    from matching.gpt_anchor_suggester import suggest_anchor
    import random
    import os
    from tqdm import tqdm
    from urllib.parse import urlparse, urldefrag
    from db.supabase_client import get_supabase
    import ast
    import openai
    import logging
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv

    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    def remove_hyperlinked_text(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        for a in soup.find_all("a"):
            a.decompose()  # Removes the <a> tag and its contents
        return soup.get_text()


    def get_blogs_for_seed(seed_url):
        supabase = get_supabase()
        return supabase.table("blogs").select("*").eq("url", seed_url).execute().data

    def get_blog_by_url(url):
        supabase = get_supabase()
        data = supabase.table("blogs").select("*").eq("url", url).execute().data
        return data[0] if data else None

    def insert_blog(blog):
        supabase = get_supabase()
        existing = get_blog_by_url(blog["url"])
        if not existing:
            supabase.table("blogs").insert(blog).execute()

    def get_blog_pattern(input_url):
        # Example: https://vitacleanhq.com/blogs/the-vitaclean-blog/kicking-the-chlorine...
        parsed = urlparse(input_url)
        path_parts = parsed.path.strip("/").split("/")
        # Assume the blog pattern is up to the second-to-last segment
        if len(path_parts) > 1:
            pattern = "/" + "/".join(path_parts[:-1]) + "/"
        else:
            pattern = parsed.path
        return pattern

    def is_valid_blog_url(url, pattern):
        url, _ = urldefrag(url)  # Remove fragment
        parsed = urlparse(url)
        path = parsed.path

        # Must start with the pattern
        if not path.startswith(pattern):
            return False

        # Must not be the index page (should have a slug after the pattern)
        if path.rstrip("/") == pattern.rstrip("/"):
            return False

        # Exclude paginated or query URLs
        if "/page/" in path or "-page-" in path or "?page=" in url or parsed.query:
            return False

        # Exclude URLs ending with /blogs or /blogs/
        if path.rstrip("/").endswith("/blogs"):
            return False

        # Must be HTTP/HTTPS
        if not parsed.scheme.startswith("http"):
            return False

        return True

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # 1. Prompt for input URL and derive seed
    pattern = get_blog_pattern(input_url)
    seed_url = input_url[:input_url.find(pattern) + len(pattern)]
    # Now use seed_url to start crawling

    # 2. Check if all blogs for this seed exist in DB
    supabase = get_supabase()
    blogs = supabase.table("blogs").select("*").like("url", f"{seed_url}%").execute().data

    # 3. Check if input blog exists in DB
    input_blog_db = get_blog_by_url(input_url)

    # 4. If all blogs exist and input blog exists, skip crawling/embedding
    if blogs and input_blog_db:
        print("✅ Using cached blogs from Supabase.")
    else:
        # If not, crawl and insert missing blogs
        if not blogs:
            print("🔎 Crawling and extracting all blogs for this site...")
            urls = crawl_blog_urls(seed_url, path_prefix=(pattern,))

            # Normalize: remove fragments and deduplicate
            def normalize_url(url):
                url, _ = urldefrag(url)
                return url

            urls = list({normalize_url(u) for u in urls})

            filtered_urls = [u for u in urls if is_valid_blog_url(u, pattern)]
            filtered_urls = list(set(filtered_urls))  # Deduplicate again, just in case

            print(f"\nFound {len(filtered_urls)} blog URLs after filtering:")
            for url in filtered_urls:
                print("-", url)

            print("\nExtracting content...\n")
            extracted = [extract_blog_data(url) for url in tqdm(filtered_urls, desc="Extracting blog content")]
            blogs = [b for b in extracted if b]
            # Filter out blogs with titles indicating index pages
            def is_article_title(title):
                return not any([
                    "Page" in title,
                    "Index" in title,
                    "Archive" in title,
                ])

            blogs = [b for b in blogs if is_article_title(b["title"])]

            print(f"\n✅ Extracted {len(blogs)} valid blog posts.")

            for blog in blogs:
                sentences = clean_text(blog["content"])
                blog["sentences"] = sentences

            print(f"\n✅ Sentence split complete.")
            print(f"Example from first blog:\n")
            print(f"Title: {blogs[0]['title']}")
            for s in blogs[0]["sentences"][:5]:
                print("-", s)
            print("\n🔗 Generating embeddings from OpenAI...\n")
            embedded_blogs = [embed_blog(blog) for blog in tqdm(blogs)]
            for blog in tqdm(blogs):
                blog["embedding"] = get_embedding(blog["title"] + "\n\n" + blog["content"])
                blog["seed_url"] = seed_url
                insert_blog(blog)
        if not input_blog_db:
            print("➕ Extracting and embedding the input blog...")
            blog = extract_blog_data(input_url)
            if blog:
                blog["embedding"] = get_embedding(blog["title"] + "\n\n" + blog["content"])
                blog["seed_url"] = seed_url
                insert_blog(blog)
                blogs.append(blog)

    # 5. Fetch all blogs for this seed (including the new one)
    blogs = supabase.table("blogs").select("*").like("url", f"{seed_url}%").execute().data
    input_blog = get_blog_by_url(input_url)

    # 6. Matching & Suggestion (use your existing logic)
    # Example: Compute similarity using pgvector or locally
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    dataset_vectors = np.array([ast.literal_eval(b["embedding"]) for b in blogs if b["url"] != input_url])
    input_vector = np.array(ast.literal_eval(input_blog["embedding"])).reshape(1, -1)
    sims = cosine_similarity(input_vector, dataset_vectors)[0]

    # --- Step 3: Get top 3 most similar blogs (excluding self/duplicates) ---
    # Optionally, skip if input_url is already in your dataset
    top_indices = np.argsort(sims)[::-1]
    top_matches = []
    seen_slugs = set()
    print("\nTop 5 cosine similarity matches:")
    count = 0
    for idx in top_indices:
        if blogs[idx]["slug"] == input_blog["slug"]:
            continue
        if blogs[idx]["slug"] in seen_slugs:
            continue
        seen_slugs.add(blogs[idx]["slug"])
        score = sims[idx]
        print(f"{count+1}. {blogs[idx]['title']} (slug: {blogs[idx]['slug']}) - Score: {score:.4f}")
        top_matches.append(blogs[idx])
        count += 1
        if count == 5:
            break

    # For anchor suggestions, use only the top 3
    top_matches = top_matches[:3]

    # --- Step 4: Generate anchor suggestions ---
    def is_relevant_paragraph(paragraph):
        if not paragraph or len(paragraph.strip()) < 50:
            return False
        irrelevant_phrases = [
            "your cart is currently empty",
            "no posts found",
            "404 not found",
            "page not found",
            "subscribe to our newsletter"
        ]
        para_lower = paragraph.lower()
        return not any(phrase in para_lower for phrase in irrelevant_phrases)

    # If input_blog["content"] is HTML, remove hyperlinked text
    clean_content = remove_hyperlinked_text(input_blog["content_html"])
    max_chars = 6000
    full_content = clean_content[:max_chars]

    anchor_suggestions = []
    for match in top_matches:
        gpt_result = suggest_anchor(input_blog["title"], full_content, match["title"])
        print(f"\n🔗 {input_blog['title']} ➜ {match['title']}")
        print(f"Target Link   : {match['url']}")
        # gpt_result["suggestions"] is a list of dicts
        for suggestion in gpt_result.get("suggestions", []):
            print(f"Anchor Sentence: {suggestion['sentence']}")
            print(f"Anchor Text   : {suggestion['anchor_text']}")
            anchor_suggestions.append({
                "target_link": match["url"],
                "anchor_sentence": suggestion["sentence"],
                "anchor_text": suggestion["anchor_text"]
            })

    return {
        "anchor_suggestions": anchor_suggestions
    }


