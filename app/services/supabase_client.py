
import os
from supabase import create_client, Client
import httpx
from fastapi import HTTPException

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY)

def get_user_from_token(authorization: str | None):
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1]
    # Verify with Supabase auth
    auth_url = f"{SUPABASE_URL}/auth/v1/user"
    headers = {"Authorization": f"Bearer {token}", "apikey": SUPABASE_ANON_KEY}
    with httpx.Client() as client:
        r = client.get(auth_url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()

def require_admin(authorization: str | None):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    uid = user["id"]
    # check profiles.role
    resp = supabase.table("profiles").select("role").eq("id", uid).maybe_single().execute()
    role = (resp.data or {}).get("role")
    if role != "admin" and role != "moderator":
        raise HTTPException(status_code=403, detail="Admin only")
    return True
