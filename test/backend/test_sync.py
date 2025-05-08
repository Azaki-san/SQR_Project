import pytest, time
from fastapi import UploadFile, HTTPException
from fastapi.testclient import TestClient
from app.services import sync
from app.main import app

client = TestClient(app)


class DummyUploadFile:
    def __init__(self, filename, content_type, content: bytes):
        self.filename = filename
        self.content_type = content_type
        self._content = content

    async def read(self):
        return self._content


@pytest.fixture(autouse=True)
def reset_state():
    sync._state.update(filename=None, start_time=None, expected_end=None)
    yield
    sync._state.update(filename=None, start_time=None, expected_end=None)


def test_validate_upload_valid():
    file = DummyUploadFile("video.mp4", "video/mp4", b"fake content")
    sync._validate_upload(file)  # should not raise


def test_validate_upload_invalid_extension():
    file = DummyUploadFile("video.txt", "text/plain", b"")
    with pytest.raises(HTTPException) as exc:
        sync._validate_upload(file)
    assert exc.value.status_code == 400


def test_validate_upload_wrong_content_type():
    file = DummyUploadFile("video.mp4", "video/quicktime", b"")
    with pytest.raises(HTTPException) as exc:
        sync._validate_upload(file)
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_upload_video_success(mocker, tmp_path):
    dummy_path = tmp_path / "video.mp4"

    # Mock ffmpeg
    mocker.patch("app.services.sync._ensure_ffmpeg", return_value=None)
    mocker.patch("app.services.sync.subprocess.run", return_value=mocker.Mock(returncode=0, stderr=""))
    mocker.patch("app.services.sync._parse_duration", return_value=5.0)
    mocker.patch("app.services.sync.VIDEO_DIR", tmp_path)

    file = DummyUploadFile("video.mp4", "video/mp4", b"fake content")
    result = await sync.upload_video(file)

    assert result["message"] == "video uploaded"
    assert dummy_path.exists()


def test_get_video_status_idle():
    status = sync.get_video_status()
    assert status == {"status": "idle"}


def test_get_video_status_playing(mocker):
    sync._state.update(filename="video.mp4", start_time=time.time(), expected_end=time.time() + 10)
    mocker.patch("app.services.sync.get_viewer_count", return_value=42)
    status = sync.get_video_status()
    assert status["status"] == "playing"
    assert status["filename"] == "video.mp4"
    assert status["viewers"] == 42


def test_get_video_filename_path_not_playing():
    with pytest.raises(HTTPException) as exc:
        sync.get_video_filename_path()
    assert exc.value.status_code == 404
