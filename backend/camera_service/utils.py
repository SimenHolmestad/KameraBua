from pathlib import Path
import subprocess
import pyautogui


def get_display_size() -> tuple[int, int]:
    default_width = 1920
    default_height = 1080

    try:
        width, height = pyautogui.size()

        if width <= 0 or height <= 0:
            return (default_width, default_height)

        return (width, height)
    except Exception:
        return (default_width, default_height)


def get_common_ffplay_parameters() -> list[str]:
    width, height = get_display_size()

    return [
        "-window_title",
        "CameraHub",
        "-noborder",
        "-left",
        "0",
        "-top",
        "0",
        "-x",
        str(width),
        "-y",
        str(height),
        "-loglevel",
        "warning",
        "-probesize",
        "32",
        "-analyzeduration",
        "0",
    ]


def show_overlay() -> subprocess.Popen[str]:
    overlay_path = Path(__file__).resolve().parent / "media" / "smil_for_faen.png"
    width, height = get_display_size()
    centered_overlay_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
    )

    return subprocess.Popen(
        [
            "ffplay",
            *get_common_ffplay_parameters(),
            "-vf",
            centered_overlay_filter,
            "-loop",
            "1",
            str(overlay_path),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def stop_process(process: subprocess.Popen[str] | None) -> None:
    if process is None:
        return

    try:
        process.terminate()
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)
    except Exception:
        process.kill()
        process.wait(timeout=2)
