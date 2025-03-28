import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from producer import send_to_queue

router = APIRouter(prefix='/upload')

@router.post('/')
async def upload_music(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    os.makedirs("tmp", exist_ok=True) 
    file_location = os.path.join("tmp", file.filename)

    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    await send_to_queue(file_location)
    return {"status": "uploaded", "file": file.filename}