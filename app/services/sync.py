import time
from pathlib import Path

from fastapi import HTTPException, UploadFile
from typing import Final
from pymediainfo import MediaInfo

from app.utils.viewer_count import get_viewer_count

VIDEO_DIR: Final[Path] = Path("shared_video")  # writable, persisted via volume
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

_state: dict[str, float | str | None] = {
    "filename": None,  # str | None
    "start_time": None,  # float | None  (epoch seconds)
    "expected_end": None,  # float | None
}


def _expire_if_finished() -> None:
    """Clear state when playback time runs out."""
    if _state["expected_end"] and time.time() >= _state["expected_end"]:
        _state.update(filename=None, start_time=None, expected_end=None)


def get_video_filename_path() -> tuple[str, str]:
    """Return (abs_path, filename) or 404 if nothing is playing."""
    _expire_if_finished()
    if not _state["filename"]:
        raise HTTPException(404, "No video playing")
    path = VIDEO_DIR / _state["filename"]
    return str(path), _state["filename"]


def get_video_status() -> dict:
    """Return status for /status endpoint."""
    _expire_if_finished()
    if not _state["filename"]:
        return {"status": "idle"}

    elapsed = time.time() - float(_state["start_time"])  # type: ignore
    return {
        "status": "playing",
        "filename": _state["filename"],
        "elapsed": elapsed,
        "viewers": get_viewer_count(),
    }


async def upload_video(file: UploadFile) -> dict:
    """Save, validate and start playback. 409 if something is already playing."""
    _expire_if_finished()
    if _state["filename"]:
        raise HTTPException(409, "A video is already playing")

    target = VIDEO_DIR / file.filename
    target.write_bytes(await file.read())

    try:
        duration = _parse_duration(target)
    except HTTPException:
        target.unlink(missing_ok=True)
        raise

    now = time.time()
    _state.update(filename=file.filename, start_time=now, expected_end=now + duration)

    return {"message": "video uploaded", "filename": file.filename, "duration": duration}


def _parse_duration(path: Path) -> float:
    media = MediaInfo.parse(path)
    for tr in media.tracks:
        if tr.track_type == "Video" and tr.duration:
            return float(tr.duration) / 1000.0
    raise HTTPException(400, "No video track found")
