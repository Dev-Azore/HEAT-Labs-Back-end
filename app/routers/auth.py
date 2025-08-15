import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Initialize Supabase client with service role key (backend only)
# Use anon key for frontend endpoints
def get_supabase_client(use_service_role: bool = True) -> Client:
    key = SUPABASE_SERVICE_ROLE_KEY if use_service_role else SUPABASE_ANON_KEY
    if not SUPABASE_URL or not key:
        raise ValueError("Missing Supabase credentials in .env")
    return create_client(SUPABASE_URL, key)

# Example usage
if __name__ == "__main__":
    # Backend example: using service role key
    supabase = get_supabase_client()
    print("Connected to Supabase with Service Role key.")
