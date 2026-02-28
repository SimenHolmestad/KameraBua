import os
import signal
import subprocess
import time
from typing import Optional
from urllib import request, error


OPENAPI_URL = "http://localhost:5000/openapi.json"
BACKEND_LOG_PATH = "/tmp/camerahub-backend.log"
WAIT_SECONDS = 30


def _repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _start_backend() -> subprocess.Popen:
    print("Starting backend for OpenAPI generation...")
    log_handle = open(BACKEND_LOG_PATH, "w")
    env = os.environ.copy()
    env["CAMERAHUB_BACKEND_PORT"] = "5000"
    return subprocess.Popen(
        ["python3", "-m", "scripts.run_backend"],
        stdout=log_handle,
        stderr=log_handle,
        env=env
    )


def _wait_for_backend(url: str, timeout_seconds: int) -> bool:
    print(f"Waiting for backend at {url}...")
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with request.urlopen(url, timeout=2):
                return True
        except (error.URLError, error.HTTPError):
            time.sleep(1)
    return False


def _run_type_generation(frontend_dir: str) -> None:
    print("Generating frontend API client...")
    subprocess.check_call(["npm", "run", "gen:api"], cwd=frontend_dir)


def _terminate_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    print("Stopping backend...")
    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    repo_root = _repo_root()
    backend_proc: Optional[subprocess.Popen] = None

    try:
        backend_proc = _start_backend()
        if not _wait_for_backend(OPENAPI_URL, WAIT_SECONDS):
            print("Backend did not start in time. Log output:")
            try:
                with open(BACKEND_LOG_PATH, "r") as log_handle:
                    print(log_handle.read())
            except OSError as exc:
                print(f"Could not read backend log: {exc}")
            return 1

        frontend_dir = os.path.join(repo_root, "frontend")
        _run_type_generation(frontend_dir)
        print("Frontend API client generation complete.")
        return 0
    finally:
        if backend_proc:
            _terminate_process(backend_proc)


if __name__ == "__main__":
    raise SystemExit(main())
