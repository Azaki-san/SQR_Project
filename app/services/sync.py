import time
from pathlib import Path

from fastapi import HTTPException
from typing import Final

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
        "status":  "playing",
        "filename": _state["filename"],
        "elapsed": elapsed,
        "viewers": get_viewer_count(),
    }
