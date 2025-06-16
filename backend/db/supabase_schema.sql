-- Enable pgvector extension
create extension if not exists vector;

-- Blog table
create table blogs (
  id uuid primary key default gen_random_uuid(),
  url text unique not null,
  title text,
  slug text,
  content text,
  embedding vector(1536),
  created_at timestamp default now(),
  seed_url text
);

-- Link suggestions table
create table link_suggestions (
  id uuid primary key default gen_random_uuid(),
  source_blog_id uuid references blogs(id),
  target_blog_id uuid references blogs(id),
  suggestion_json jsonb,
  created_at timestamp default now()
);

-- Optional: index for fast ANN search
create index on blogs using ivfflat (embedding vector_cosine_ops) with (lists = 100);

select *, embedding <=> '[...]' as similarity
from blogs
where url like 'https://example.com/blog/%'
order by embedding <=> '[...]'
limit 5;
