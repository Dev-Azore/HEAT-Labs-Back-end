from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(username: str, password: str):
    # Dummy authentication logic
    if username == "admin" and password == "password":
        return {"message": "Login successful", "user": username}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@router.post("/logout")
def logout():
    return {"message": "Logout successful"}
