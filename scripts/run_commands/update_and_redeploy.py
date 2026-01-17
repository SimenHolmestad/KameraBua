import os
import subprocess
from .deploy import Deploy


class UpdateAndRedeploy(Deploy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        if os.geteuid() != 0:
            print("The update and redploy script must be run as root.")
            print("Run script with \"sudo python3 update_and_redeploy\"")
            return

        subprocess.run("git reset --hard HEAD", shell=True)
        subprocess.run("git pull", shell=True)
        self.build_frontend()

        systemd_file_content = ""
        systemd_file_path = self.get_systemd_file_path()
        with open(systemd_file_path, "r") as f:
            systemd_file_content = f.read()
        print("--------Systemd file is--------")
        print(systemd_file_content)
        print("-------------------------------")

        self.start_or_restart_systemd_process()
        print("System started")
        print("To get system status, run \"sudo systemctl status camerahub\"")
        print("To get last log lines, run \"journalctl --unit=camerahub -n 100 --no-pager\"")
