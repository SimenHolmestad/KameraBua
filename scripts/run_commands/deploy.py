import os
import subprocess
from .base_run_config import BaseRunConfig


class Deploy(BaseRunConfig):
    """Deploy the application to Systemd."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        if os.geteuid() != 0:
            print("The deploy script must be run as root.")
            print("Run script with \"sudo python3 deploy ...\"")
            return

        if not self.frontend_is_built():
            self.build_frontend()

        application_command = self.get_application_command_from_raw_args()
        systemd_file_content = self.create_systemd_config_file_content(application_command)
        print("--------Systemd file is--------")
        print(systemd_file_content)
        print("-------------------------------")

        systemd_file_path = self.get_systemd_file_path()
        print("Writing file to", systemd_file_path)
        with open(systemd_file_path, "w") as f:
            f.write(systemd_file_content)

        self.start_or_restart_systemd_process()
        print("System started")
        print("To get system status, run \"sudo systemctl status camerahub\"")
        print("To get last log lines, run \"journalctl --unit=camerahub -n 100 --no-pager\"")

    def get_systemd_file_path(self):
        return os.path.join(
            "/",
            "etc",
            "systemd",
            "system",
            "camerahub.service"
        )

    def start_or_restart_systemd_process(self):
        subprocess.run("sudo systemctl daemon-reload", shell=True)
        # Restart in this case should start the system if it is not
        # already started
        subprocess.run("sudo systemctl restart camerahub", shell=True)

    def create_systemd_config_file_content(self, application_command):
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
            "ExecStart={}".format(application_command),
            "Restart=always",
            "",
            "[Install]",
            "WantedBy=multi-user.target"
        ]
        return "\n".join(content_lines)

    def get_application_command_from_raw_args(self):
        def change_deploy_arg_to_run_app(arg):
            if arg == "deploy":
                return "run_application"
            return arg

        application_args = list(map(change_deploy_arg_to_run_app, self.raw_args))
        return "python3 " + " ".join(application_args)
