import time
import pytest
from freezegun import freeze_time

from app.utils.viewer_count import viewer_ping, get_viewer_count, _viewers

@pytest.fixture(autouse=True)
def clear_viewers():
    _viewers.clear()
    yield
    _viewers.clear()

def test_single_viewer():
    viewer_ping("viewer1")
    assert get_viewer_count() == 1

def test_multiple_viewers():
    viewer_ping("a")
    viewer_ping("b")
    viewer_ping("c")
    assert get_viewer_count() == 3

def test_viewer_timeout():
    with freeze_time() as frozen:
        viewer_ping("old_viewer")
        frozen.tick(16)
        assert get_viewer_count() == 0

def test_viewer_refresh():
    with freeze_time() as frozen:
        viewer_ping("v1")
        frozen.tick(10)
        viewer_ping("v1")
        frozen.tick(10)
        assert get_viewer_count() == 1
