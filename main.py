# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware

app = FastAPI()

# ⚠️ CORS Configuration: Allows the frontend (FE) domain to access the API.
# This is crucial when the FE (Vercel) and BE (GCP Cloud Run) are on different domains.
origins = [
    "http://localhost:3000", # FE development server
    "https://[your-vercel-domain].vercel.app", # FE production domain (MUST BE UPDATED)
    "https://lilyinit.github.io", # GitHub Pages portfolio domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Lily AI Backend API is running!"}