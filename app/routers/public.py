
from fastapi import APIRouter, HTTPException
from ..services.supabase_client import supabase

router = APIRouter(prefix="/public", tags=["public"])

@router.get("/labs")
def labs():
    r = supabase.table("courses").select("*").order("sort_order").execute()
    return {"labs": r.data}

@router.get("/modules/{module_id}")
def module_by_id(module_id:int):
    r = supabase.table("modules").select("*").eq("id", module_id).maybe_single().execute()
    if not r.data:
        raise HTTPException(status_code=404, detail="Not found")
    return {"module": r.data}

@router.get("/modules-by-lab/{lab_id}")
def modules_by_lab(lab_id:int):
    r = supabase.table("modules").select("*").eq("course_id", lab_id).order("sort_order").execute()
    return {"modules": r.data}
