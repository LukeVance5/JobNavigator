from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import jobs

# 1. Initialize the App
app = FastAPI(
    title="Job Navigator API",
    version="1.0.0",
    description="AI-powered job search and resume management",
    docs_url="/api/docs",  # Custom docs path for security
)

# 2. Setup CORS (Crucial for React frontend to talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Register Routers (The "Plugs")
# We add a prefix so our URLs look like /api/v1/jobs
API_PREFIX = "/api/v1"

app.include_router(jobs.router, prefix=f"{API_PREFIX}/jobs", tags=["Jobs"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Job Navigator API", "status": "online"}
