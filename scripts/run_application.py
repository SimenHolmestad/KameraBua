from backend.config_loader import load_settings
from backend.settings import Settings
from scripts.shared.utils import (
    PRODUCTION_PORT,
    build_frontend,
    create_app_with_settings,
    find_ip_address_for_device,
    frontend_is_built,
    get_url_for_qr_code_page,
    open_webpage_in_device_browser,
)


def run_application(settings: Settings) -> None:
    if not frontend_is_built():
        build_frontend()

    host_ip = find_ip_address_for_device()
    qr_code_url = get_url_for_qr_code_page(host_ip, PRODUCTION_PORT, settings.albums.forced_album)
    print("Url for qr codes:", qr_code_url)

    app = create_app_with_settings(settings, host_ip, PRODUCTION_PORT)

    browser_process = open_webpage_in_device_browser(qr_code_url)
    app.run(host=host_ip)

    # Delete browser process if it was created
    if browser_process:
        browser_process.terminate()


def main() -> None:
    settings = load_settings()
    run_application(settings)


if __name__ == '__main__':
    main()
