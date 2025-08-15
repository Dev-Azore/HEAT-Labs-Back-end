from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from supabase import create_client
import os

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://knjhqjygkplullnsqmdk.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtuamhxanlna3BsdWxsbnNxbWRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ5NDA1NTgsImV4cCI6MjA3MDUxNjU1OH0.VI-XbbWnxW5GMqhsoaUTGidGJ2nR9xa-DkFujvmxNLE")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    # Sign in with email and password
    result = supabase.auth.sign_in_with_password({
        "email": data.email,
        "password": data.password
    })

    if result.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {
        "message": "Login successful",
        "user": {
            "id": result.user.id,
            "email": result.user.email
        },
        "access_token": result.session.access_token
    }

@router.post("/logout")
def logout():
    return {"message": "Logout successful"}
