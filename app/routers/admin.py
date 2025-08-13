
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional, Dict, Any
from ..services.supabase_client import supabase, get_user_from_token, require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/labs")
def list_labs(authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("courses").select("*").order("sort_order").execute()
    return {"labs": resp.data}

@router.post("/labs")
def create_lab(lab: Dict[str, Any], authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("courses").insert(lab).execute()
    return {"created": resp.data}

@router.patch("/labs/{lab_id}")
def update_lab(lab_id: int, lab: Dict[str, Any], authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("courses").update(lab).eq("id", lab_id).execute()
    return {"updated": resp.data}

@router.delete("/labs/{lab_id}")
def delete_lab(lab_id: int, authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("courses").delete().eq("id", lab_id).execute()
    return {"deleted": resp.data}

@router.get("/modules/{lab_id}")
def list_modules(lab_id: int, authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("modules").select("*").eq("course_id", lab_id).order("sort_order").execute()
    return {"modules": resp.data}

@router.post("/modules")
def create_module(module: Dict[str, Any], authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("modules").insert(module).execute()
    return {"created": resp.data}

@router.patch("/modules/{module_id}")
def update_module(module_id: int, module: Dict[str, Any], authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("modules").update(module).eq("id", module_id).execute()
    return {"updated": resp.data}

@router.delete("/modules/{module_id}")
def delete_module(module_id: int, authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("modules").delete().eq("id", module_id).execute()
    return {"deleted": resp.data}

# Resources CRUD for admin
@router.get("/resources")
def list_resources(authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("resources").select("*").order("created_at", desc=True).execute()
    return {"resources": resp.data}

@router.post("/resources")
def create_resource(item: Dict[str, Any], authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("resources").insert(item).execute()
    return {"created": resp.data}

@router.delete("/resources/{rid}")
def delete_resource(rid: int, authorization: Optional[str] = Header(None)):
    require_admin(authorization)
    resp = supabase.table("resources").delete().eq("id", rid).execute()
    return {"deleted": resp.data}
