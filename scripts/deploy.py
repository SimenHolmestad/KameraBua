import os
import subprocess
from scripts.shared.utils import build_frontend, frontend_is_built


def run_deploy() -> None:
    """Deploy the application to Systemd."""
    if os.geteuid() != 0:
        print("The deploy script must be run as root.")
        print("Run script with \"sudo python3 scripts/deploy.py\"")
        return

    if not frontend_is_built():
        build_frontend()

    systemd_file_content = create_systemd_config_file_content()
    print("--------Systemd file is--------")
    print(systemd_file_content)
    print("-------------------------------")

    systemd_file_path = get_systemd_file_path()
    print("Writing file to", systemd_file_path)
    with open(systemd_file_path, "w") as f:
        f.write(systemd_file_content)

    start_or_restart_systemd_process()
    print("System started")
    print("To get system status, run \"sudo systemctl status camerahub\"")
    print("To get last log lines, run \"journalctl --unit=camerahub -n 100 --no-pager\"")


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


def create_systemd_config_file_content() -> str:
    username = os.environ["SUDO_USER"]
    working_directory = os.getcwd()

    content_lines = [
        "[Unit]",
        "Description=Camerahub",
        "After=network.target",
        "",
        "[Service]",
        "User={}".format(username),
        "WorkingDirectory={}".format(working_directory),
        "ExecStart=python3 scripts/run_application.py"
        "Restart=always",
        "",
        "[Install]",
        "WantedBy=multi-user.target"
    ]
    return "\n".join(content_lines)


if __name__ == "__main__":
    run_deploy()
