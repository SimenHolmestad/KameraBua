from backend.config_loader import load_settings
from backend.settings import Settings
from scripts.shared.utils import (
    DEBUG_PORT,
    create_app_with_settings,
    find_ip_address_for_device,
    get_url_for_qr_code_page,
)


def run_backend(settings: Settings) -> None:
    """This should only need to be done when working on or testing the frontend."""
    print("Running the backend in debug mode. Start the frontend in a separate terminal window")

    host_ip = find_ip_address_for_device()
    qr_code_url = get_url_for_qr_code_page(host_ip, DEBUG_PORT, settings.albums.forced_album)
    print("Url for qr codes (when frontend is running):", qr_code_url)

    app = create_app_with_settings(settings, host_ip, DEBUG_PORT)
    app.run(debug=True, host="localhost")


def main() -> None:
    settings = load_settings()
    run_backend(settings)


if __name__ == "__main__":
    main()
