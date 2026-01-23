import argparse
import os
import subprocess
from backend.core.config_loader import load_config
from scripts.shared.utils import build_frontend, frontend_is_built


def run_deploy(config_path: str) -> None:
    """Deploy the application to Systemd."""
    if os.geteuid() != 0:
        print("The deploy script must be run as root.")
        print("Run script with \"sudo .venv/bin/python scripts/deploy.py\"")
        return

    config = load_config(config_path)
    static_folder_name = config.static_folder_name
    if not frontend_is_built(static_folder_name):
        build_frontend(static_folder_name)

    systemd_file_content = create_systemd_config_file_content(config_path)
    print("--------Systemd file is--------")
    print(systemd_file_content)
    print("-------------------------------")

    systemd_file_path = get_systemd_file_path()
    print("Writing file to", systemd_file_path)
    with open(systemd_file_path, "w") as f:
        f.write(systemd_file_content)

    ensure_static_permissions(static_folder_name)
    start_or_restart_systemd_process()
    print("System started")
    print("To get system status, run \"sudo systemctl status camerahub\"")
    print("To get last log lines, run \"journalctl --unit=camerahub -n 100 --no-pager\"")
    print("To stop the deployment, run \"sudo systemctl stop camerahub\"")


def get_systemd_file_path() -> str:
    return os.path.join(
        "/",
        "etc",
        "systemd",
        "system",
        "camerahub.service"
    )


def start_or_restart_systemd_process() -> None:
    subprocess.run("sudo systemctl daemon-reload", shell=True)
    # Restart in this case should start the system if it is not already started
    subprocess.run("sudo systemctl restart camerahub", shell=True)


def create_systemd_config_file_content(config_path: str) -> str:
    username = os.environ["SUDO_USER"]
    working_directory = os.getcwd()
    resolved_config_path = _resolve_config_path(working_directory, config_path)

    content_lines = [
        "[Unit]",
        "Description=Camerahub",
        "After=network.target",
        "",
        "[Service]",
        f"User={username}",
        f"WorkingDirectory={working_directory}",
        f"ExecStart={working_directory}/.venv/bin/python -m scripts.run_application --config {resolved_config_path}",
        "Restart=always",
        "",
        "[Install]",
        "WantedBy=multi-user.target"
    ]
    return "\n".join(content_lines)


def ensure_static_permissions(static_folder_name: str) -> None:
    username = os.environ["SUDO_USER"]
    working_directory = os.getcwd()
    static_dir = os.path.join(working_directory, "backend", static_folder_name)
    os.makedirs(static_dir, exist_ok=True)
    subprocess.run(
        ["chown", "-R", f"{username}:{username}", static_dir],
        check=True
    )

def _resolve_config_path(working_directory: str, config_path: str) -> str:
    if os.path.isabs(config_path):
        return config_path
    return os.path.join(working_directory, config_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy CameraHub as a systemd service.")
    parser.add_argument(
        "--config",
        default=os.path.join("configs", "example_config.json"),
        help="Path to config file to use for the systemd service."
    )
    args = parser.parse_args()
    run_deploy(args.config)
