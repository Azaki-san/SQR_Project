from fastapi import APIRouter, UploadFile, Request
from app.services.sync import get_video_filename_path
from fastapi.responses import FileResponse

from app.utils.viewer_count import viewer_ping, get_viewer_count

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
