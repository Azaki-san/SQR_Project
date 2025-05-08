import time
from pathlib import Path

from fastapi import HTTPException

VIDEO_DIR = Path("shared_video")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

_video_state: dict[str, float | str | None] = {
    "filename": None,  # str | None
    "start_time": None,  # float | None (epoch seconds)
    "expected_end": None,  # float | None
}


def _expire_if_finished() -> None:
    """Clear state when the current video has finished playing."""
    if _video_state["expected_end"] and time.time() >= _video_state["expected_end"]:
        _video_state.update(filename=None, start_time=None, expected_end=None)


def get_video_filename_path() -> tuple[str, str]:
    """Return (absolute_path, filename) for the current file or 404."""
    _expire_if_finished()
    if not _video_state["filename"]:
        raise HTTPException(status_code=404, detail="No video playing")
    path = VIDEO_DIR / _video_state["filename"]
    return str(path), _video_state["filename"]
