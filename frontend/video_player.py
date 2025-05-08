from streamlit.components.v1 import html  # type: ignore
from api import BACKEND_URL

def render_video_player(filename, elapsed):
    video_url = f"{BACKEND_URL}/videos/{filename}"
    video_html = f"""
    <link href="https://vjs.zencdn.net/8.5.2/video-js.css" rel="stylesheet" />
    <script src="https://vjs.zencdn.net/8.5.2/video.min.js"></script>

    <style>
      /* Hide everything except volume and time display */
      .video-js .vjs-play-control,
      .video-js .vjs-fullscreen-control,
      .video-js .vjs-progress-control,
      .video-js .vjs-playback-rate,
      .video-js .vjs-big-play-button {{
        display: none !important;
      }}
    </style>

    <video
      id="syncedVideo"
      class="video-js vjs-default-skin"
      controls
      preload="auto"
      width="700"
      height="400">
      <source src="{video_url}" type="video/mp4" />
      Your browser does not support the video tag.
    </video>

    <div id="viewersCount" style="font-size:18px;color:blue;margin-top:15px;"></div>

    <script>
    const backend = "{BACKEND_URL}";
    const viewersCount = document.getElementById("viewersCount");

    const player = videojs('syncedVideo', {{
        autoplay: true,
        muted: false,
        preload: 'auto',
        controlBar: {{
            children: [
                'volumePanel',
                'currentTimeDisplay',
                'timeDivider',
                'durationDisplay'
            ]
        }}
    }});

    player.ready(function () {{
        const seekTime = {elapsed};
        player.currentTime(seekTime);
        player.play().catch(err => {{
            console.error("Autoplay failed:", err);
        }});

        // Force playbackRate and prevent pause
        player.playbackRate(1);
        player.on("ratechange", () => {{
            player.playbackRate(1);
        }});

        player.on("pause", () => {{
            player.play().catch(err => {{
                console.error("Autoplay retry failed:", err);
            }});
        }});
    }});

    // Sync with backend
    setInterval(async () => {{
        try {{
            const r = await fetch(backend + "/status");
            if (!r.ok) return;
            const d = await r.json();
            if (d.status === "playing") {{
                const current = player.currentTime();
                const target = Math.floor(d.elapsed);
                if (Math.abs(current - target) > 2) {{
                    player.currentTime(target);
                    console.log("Resync → " + target + " s");
                }}
                viewersCount.textContent = "Viewers: " + d.viewers;
            }}
        }} catch (err) {{
            console.error("Sync failed:", err);
        }}
    }}, 1000);

    // Regular ping to backend to notify viewer is watching
    setInterval(async () => {{
        try {{
            await fetch(backend + "/ping", {{
                method: "POST"
            }});
        }} catch (err) {{
            console.error("Ping failed:", err);
        }}
    }}, 10000);
    </script>
    """
    html(video_html, height=780, scrolling=False)
