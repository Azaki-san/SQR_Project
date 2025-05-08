from fastapi import APIRouter, UploadFile, Request
from app.services.sync import get_video_filename_path
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/video")
def get_video_file():
    path, filename = get_video_filename_path()
    return FileResponse(path, media_type="video/mp4", filename=filename)
