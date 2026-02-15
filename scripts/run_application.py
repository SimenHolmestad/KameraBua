import argparse
import os
import uvicorn
from backend.core.config_loader import load_config
from backend.core.config import Config
from scripts.shared.utils import (
    PRODUCTION_PORT,
    build_frontend,
    create_app_with_config,
    find_ip_address_for_device,
    frontend_is_built,
    get_url_for_qr_code_page,
    open_webpage_in_device_browser,
)


def run_application(config: Config) -> None:
    if not frontend_is_built(config.static_folder_name):
        build_frontend(config.static_folder_name)

    host_ip = find_ip_address_for_device()
    qr_code_url = get_url_for_qr_code_page(host_ip, PRODUCTION_PORT, config.albums.forced_album)
    print("Url for qr codes:", qr_code_url)

    app = create_app_with_config(config, host_ip, PRODUCTION_PORT)

    browser_process = open_webpage_in_device_browser(qr_code_url)
    uvicorn.run(app, host=host_ip, port=PRODUCTION_PORT)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CameraHub application.")
    parser.add_argument(
        "--env-file",
        dest="env_file",
        default=None,
        help="Path to a .env file."
    )
    args = parser.parse_args()
    env_file = args.env_file or os.path.join(".env")
    config = load_config(env_file)
    run_application(config)


if __name__ == '__main__':
    main()
