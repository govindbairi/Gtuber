from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import yt_dlp

app = FastAPI()

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the static directory exists or update the path if different
app.mount("/static", StaticFiles(directory="static"), name="static")

cur_dir = os.getcwd()

@app.post("/download")
def download_video(link: str = Form(...)):
    youtube_dl_options = {
        "format": "best",
        "outtmpl": os.path.join(cur_dir, f"video-{link[-11:]}.mp4")  # Fixed output template
    }
    
    with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
        ydl.download([link])
    
    return {"status": "Download started"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(cur_dir, "uploaded_files", file.filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"filename": file.filename}
