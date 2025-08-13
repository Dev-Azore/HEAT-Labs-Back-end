
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional, Dict, Any
from ..services.supabase_client import supabase, get_user_from_token

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/get/{module_id}")
def get_progress(module_id: int, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = user["id"]
    # Progress table: user_id uuid, module_id int, status text, answers jsonb, updated_at timestamptz
    resp = supabase.table("progress").select("*").eq("user_id", user_id).eq("module_id", module_id).maybe_single().execute()
    return {"module_id": module_id, "progress": resp.data}

@router.post("/save/{module_id}")
def save_progress(module_id: int, payload: Dict[str, Any], authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id = user["id"]
    status = payload.get("status", "in_progress")
    answers = payload.get("answers", {})
    upsert = {
        "user_id": user_id,
        "module_id": module_id,
        "status": status,
        "answers": answers,
    }
    resp = supabase.table("progress").upsert(upsert, on_conflict="user_id,module_id").execute()
    return {"ok": True, "saved": resp.data}
