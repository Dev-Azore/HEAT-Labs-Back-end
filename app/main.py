
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import public, auth, admin, storage, progress

app = FastAPI(title="HEAT Labs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public.router)
app.include_router(auth.router)
app.include_router(storage.router)
app.include_router(admin.router)
app.include_router(progress.router)

@app.get("/health")
def health():
    return {"ok": True}
