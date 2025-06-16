import os
from supabase import create_client, Client

os.environ["SUPABASE_URL"] = "https://ibudbdxjioifobqdvdzm.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlidWRiZHhqaW9pZm9icWR2ZHptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzNTkxMjEsImV4cCI6MjA2NDkzNTEyMX0.ke5ChVlTm868aJCqXH7QMriR6UttqeLPCGUD6DRyKNc"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Use service role for insert

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
