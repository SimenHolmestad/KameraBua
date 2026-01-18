import os
import subprocess
from scripts.deploy import get_systemd_file_path, start_or_restart_systemd_process
from scripts.shared.utils import build_frontend


def run_update_and_redeploy() -> None:
    if os.geteuid() != 0:
        print("The update and redploy script must be run as root.")
        print("Run script with \"sudo python3 scripts/update_and_redeploy.py\"")
        return

    subprocess.run("git reset --hard HEAD", shell=True)
    subprocess.run("git pull", shell=True)
    build_frontend()

    systemd_file_path = get_systemd_file_path()
    with open(systemd_file_path, "r") as f:
        systemd_file_content = f.read()
    print("--------Systemd file is--------")
    print(systemd_file_content)
    print("-------------------------------")

    start_or_restart_systemd_process()
    print("System started")
    print("To get system status, run \"sudo systemctl status camerahub\"")
    print("To get last log lines, run \"journalctl --unit=camerahub -n 100 --no-pager\"")


if __name__ == "__main__":
    run_update_and_redeploy()
