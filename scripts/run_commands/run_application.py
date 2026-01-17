from .base_run_config import BaseRunConfig
from backend.app import create_app


class RunApplication(BaseRunConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        if not self.frontend_is_built():
            self.build_frontend()

        qr_code_url = self.get_url_for_qr_code_page(self.production_port)
        print("Url for qr codes:", qr_code_url)

        app = self.__initialise_app()

        browser_process = self.open_webpage_in_device_browser(qr_code_url)
        app.run(host=self.host_ip)

        # Delete browser process if it was created
        if browser_process:
            browser_process.terminate()

    def __initialise_app(self):
        qr_code_handler = self.create_qr_code_handler(self.production_port)
        album_handler = self.get_album_handler_instance()
        self.ensure_forced_album_is_created(album_handler)
        camera_module = self.get_camera_module_instance()

        return create_app(
            album_handler,
            self.static_folder_name,
            camera_module,
            qr_code_handler,
            forced_album_name=self.args.force_album
        )
