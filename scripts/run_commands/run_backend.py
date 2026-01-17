from .base_run_config import BaseRunConfig
from backend.app import create_app


class RunBackend(BaseRunConfig):
    """This should only need to be done when working on or testing the
    frontend.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        print("Running the backend in debug mode. Start the frontend in a separate terminal window")

        qr_code_url = self.get_url_for_qr_code_page(self.debug_port)
        print("Url for qr codes (when frontend is running):", qr_code_url)

        app = self.__initialise_app()
        app.run(debug=True, host="localhost")

    def __initialise_app(self):
        qr_code_handler = self.create_qr_code_handler(self.debug_port)
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
