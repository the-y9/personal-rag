from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from app.generator import generate_cover_letter, init_model
from fastapi.middleware.cors import CORSMiddleware
from visitors.tracker import router as visitor_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_model()
    yield
    # Shutdown logic (if needed)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains for more security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Mount the IP logger at /visitors
app.include_router(visitor_router, prefix="/visitors")

class JobDescription(BaseModel):
    job_description: str

@app.get("/")
def read_root():
    return {"message": "Root!"}

@app.post("/generate-cover-letter/")
def generate_endpoint(payload: JobDescription):
    try:
        if not payload.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required.")
        result = generate_cover_letter(payload.job_description)
        return {
            "message": "Cover letter generated successfully.",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
