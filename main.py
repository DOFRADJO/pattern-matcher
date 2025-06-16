from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from db import matches_col
from matching_logic import match_template_in_video_frames
import os
from utils import save_file_async

app = FastAPI(title="Pattern Matching Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload et traitement du template
@app.post("/match")
async def match_template(video_name: str = Form(...), template: UploadFile = File(...)):
    saved_path = await save_file_async(template, "templates")
    results = match_template_in_video_frames(video_name, saved_path)

    if not results:
        return {"message": "Aucune correspondance trouvée."}

    # Enregistrer dans la DB
    matches_col.insert_many(results)
    return {"matched_frames": results}
