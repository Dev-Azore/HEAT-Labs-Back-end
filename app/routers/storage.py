
from fastapi import APIRouter, Header, HTTPException, Query
from typing import Optional
from ..services.supabase_client import supabase, get_user_from_token, require_admin
import time

router = APIRouter(prefix="/storage", tags=["storage"])

@router.get("/sign-upload")
def sign_upload(bucket: str = Query(...), filename: str = Query(...), authorization: Optional[str] = Header(None)):
    # Admin only to request signed URLs for admin console uploads
    require_admin(authorization)
    # Create a signed URL for upload (Supabase storage supports upload via service key; here we return a signed URL using create_signed_upload_url if available)
    # Fallback: we will return the path; admin client will upload via POST /object using service proxy endpoint in backend (not ideal for anon).
    # Using supabase-py v2: storage.from_(bucket).create_signed_upload_url(path)
    path = f"{int(time.time())}_{filename}"
    res = supabase.storage.from_(bucket).create_signed_upload_url(path, 60 * 10)
    if not res:
        raise HTTPException(status_code=500, detail="Failed to sign upload URL")
    return { "signed_url": res["signed_url"], "path": res["path"] }
