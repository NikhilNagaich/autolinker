import openai
import os
import random
import json
import logging
import re

openai.api_key = os.getenv("OPENAI_API_KEY")

GPT_MODEL = "gpt-4-turbo"

def suggest_anchor(source_title, source_content, target_title):
    prompt = f"""
You are an intelligent SEO assistant.

We are working with the following blog post:
Current blog title: "{source_title}"
Full blog content:
\"\"\"{source_content}\"\"\"

We want to add a contextual internal link to another blog titled: "{target_title}".

Your task:
- Carefully read the content.
- Suggest up to three of the most natural, contextually relevant places to add a hyperlink to the target blog.
- For each suggestion, provide:
  - The full sentence from the content where the link would fit best.
  - A concise anchor text (3–6 words max), taken verbatim from that sentence, that is contextually relevant to the target blog.
- Do not force suggestions if no appropriate sentence exists.

Return your output strictly as a JSON object in this format:
{{
  "suggestions": [
    {{
      "sentence": "First matching sentence from the content.",
      "anchor_text": "First anchor text"
    }},
    {{
      "sentence": "Second matching sentence from the content.",
      "anchor_text": "Second anchor text"
    }},
    {{
      "sentence": "Third matching sentence from the content.",
      "anchor_text": "Third anchor text"
    }}
  ]
}}
If fewer than 3 valid suggestions exist, return only the valid ones in the "suggestions" array. If none are found, return:
{{
  "suggestions": []
}}

Do not include any explanation, markdown, or extra commentary—just the raw JSON object.
"""

    response = openai.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    raw = response.choices[0].message.content.strip()
    print("\n\n\n")
    logging.info(f"GPT raw response: {raw}")

    # Remove triple backticks and optional 'json' language tag
    cleaned = re.sub(r"^```json|^```|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        logging.error(f"Failed to parse GPT response: {e}\nRaw: {raw}\nCleaned: {cleaned}")
        return {"sentence": None, "anchor_text": None}


