from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import frames_col
from matching_logic import match_template_in_video_frames
from utils import save_file_async
import os
import httpx
import asyncio

# URL du service de découpage (scène splitter)
SPLIT_SERVICE_URL = os.getenv("SPLIT_SERVICE_URL", "http://localhost:8000")

app = FastAPI(title="Pattern Matching Service")

# Middleware CORS (autorise tous les clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/match")
async def match_template(video: UploadFile = File(...), template: UploadFile = File(...)):
    # Vérifications des formats
    if not video.filename.lower().endswith((".mp4", ".avi", ".mov")):
        raise HTTPException(status_code=400, detail="Format vidéo non supporté")
    if not template.filename.lower().endswith((".jpg", ".png", ".jpeg")):
        raise HTTPException(status_code=400, detail="Format image non supporté")

    # 📁 Sauvegarder la vidéo
    video_path = await save_file_async(video, "videos")
    video_name = os.path.basename(video_path)

    # 📤 Appel au service de découpage
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            with open(video_path, "rb") as f:
                files = {"file": (video.filename, f, "video/mp4")}
                response = await client.post(f"{SPLIT_SERVICE_URL}/detect", files=files)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Erreur lors de l'appel au service de découpage")

    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Service découpage inaccessible : {str(e)}")

    # ⏱️ Attente jusqu'à ce que les frames soient enregistrées
    timeout = 10
    while timeout > 0:
        if frames_col.count_documents({"video_name": video_name}) > 0:
            break
        await asyncio.sleep(1)
        timeout -= 1

    if timeout == 0:
        raise HTTPException(status_code=504, detail="Délai dépassé : frames non disponibles")

    # 📁 Sauvegarder le template
    template_path = await save_file_async(template, "templates")

    # 🧠 Matching
    results = match_template_in_video_frames(video_name, template_path)

    return {"matched_frames": results}
