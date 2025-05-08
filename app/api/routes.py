from fastapi import APIRouter, UploadFile, Request
from app.services.sync import get_video_filename_path, get_video_status, upload_video
from fastapi.responses import FileResponse

from app.services.weather import get_weather
from app.utils.viewer_count import viewer_ping, get_viewer_count
from app.db.database import get_video_stat, increment_video_stat

router = APIRouter()


@router.get("/video")
def get_video_file():
    path, filename = get_video_filename_path()
    return FileResponse(path, media_type="video/mp4", filename=filename)

@router.post("/ping")
def ping(request: Request):
    viewer_id = request.client.host
    viewer_ping(viewer_id)
    return {"viewers": get_viewer_count()}

@router.get("/status")
def status():
    return get_video_status()

@router.get("/weather")
def weather():
    return get_weather()

@router.get("/stats")
def stats():
    return {"total_played": get_video_stat()}

@router.post("/upload")
async def upload(file: UploadFile):
    response = await upload_video(file)
    increment_video_stat()
    return response