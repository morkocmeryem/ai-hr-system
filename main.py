from fastapi import FastAPI
from pydantic import BaseModel
from matcher import calculate_similarity
from fastapi.middleware.cors import CORSMiddleware

# Uygulama başlat
app = FastAPI()

# CORS ayarı (ileride React falan bağlanabilsin diye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# İstek modeli
class MatchRequest(BaseModel):
    cv_text: str
    job_text: str

# Yanıt modeli
class MatchResponse(BaseModel):
    similarity_score: float

# Ana endpoint
@app.post("/match", response_model=MatchResponse)
def match_texts(request: MatchRequest):
    score = calculate_similarity(request.cv_text, request.job_text)
    return {"similarity_score": score}
