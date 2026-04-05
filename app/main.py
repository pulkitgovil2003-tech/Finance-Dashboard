from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import connect_db, close_db
from app.routes import auth, users, records, dashboard


# ─── Lifespan ─────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


# ─── App Init ─────────────────────────────────────────
app = FastAPI(
    title="Finance Dashboard ",
    description="A finance dashboard backend with role based access control",
    version="1.0.0",
    lifespan=lifespan
)


# ─── CORS ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Routes ───────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


# ─── Health Check ─────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "SUCCESS",
        "message": "Finance Dashboard API is running",
        "version": "1.0.0"
    }