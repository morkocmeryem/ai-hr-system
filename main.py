from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from matcher import calculate_similarity
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uuid
import os

from affinda.parser import parse_cv
from models.schemas import ParsedCV

# Uygulama başlat
app = FastAPI()

# CORS ayarı (frontend bağlansın diye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# İstek modeli (metin karşılaştırması için)
class MatchRequest(BaseModel):
    cv_text: str
    job_text: str

# Yanıt modeli (metin karşılaştırması için)
class MatchResponse(BaseModel):
    similarity_score: float

# Endpoint: /match
@app.post("/match", response_model=MatchResponse)
def match_texts(request: MatchRequest):
    score = calculate_similarity(request.cv_text, request.job_text)
    return {"similarity_score": score}

# CV yüklemek için geçici klasör
UPLOAD_DIR = "temp_cv_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint: /upload_cv
@app.post("/upload_cv", response_model=ParsedCV)
async def upload_cv(file: UploadFile = File(...)):
    try:
        file_id = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_id)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya kaydı başarısız: {str(e)}")
    finally:
        file.file.close()

    try:
        result = await parse_cv(file_path)
        document = result.get("data", {})

        parsed = ParsedCV(
            name=document.get("name", {}).get("raw"),
            email=document.get("emails", [None])[0],
            skills=[s.get("name") for s in document.get("skills", []) if s.get("name")],
            experience=[
                {
                    "company": exp.get("organization"),
                    "position": exp.get("jobTitle"),
                    "start_date": exp.get("startDate"),
                    "end_date": exp.get("endDate")
                }
                for exp in document.get("workExperience", [])
            ]
        )
        return parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Affinda'dan cevap alınamadı: {str(e)}")

