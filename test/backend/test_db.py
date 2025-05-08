from unittest import mock
from app.db import database


@mock.patch("app.db.database.get_connection")
def test_get_video_stat(mock_get_connection):
    # mock cursor and connection
    mock_conn = mock.Mock()
    mock_cursor = mock.Mock()
    mock_cursor.fetchone.return_value = [5]
    mock_conn.execute.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    result = database.get_video_stat()

    assert result == 5
    (mock_conn.execute.
     assert_called_with("SELECT videos_played FROM stats WHERE id = 1"))
    mock_conn.close.assert_called_once()


@mock.patch("app.db.database.get_connection")
def test_increment_video_stat(mock_get_connection):
    mock_conn = mock.Mock()
    mock_get_connection.return_value = mock_conn

    database.increment_video_stat()

    mock_conn.execute.assert_called_with(
        "UPDATE stats SET videos_played = videos_played + 1 WHERE id = 1"
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
