import os
from typing import Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, Response
from backend.routers.albums import construct_album_api_router
from backend.routers.qr_codes import construct_qr_code_api_router
from backend.core.config import Config


def create_app(
    static_folder_path: str,
    config: Config,
    qr_codes: Any
) -> FastAPI:
    app = FastAPI(
        title="CameraHub API",
        version="1.0.0",
        description="API for managing albums, images, and QR codes."
    )
    if not os.path.exists(static_folder_path):
        raise RuntimeError(f"Static folder path '{static_folder_path}' does not exist")

    app.include_router(construct_album_api_router(config), prefix="/albums")

    app.include_router(construct_qr_code_api_router(qr_codes), prefix="/qr_codes")

    app.mount(
        "/static",
        StaticFiles(directory=static_folder_path),
        name="static"
    )

    @app.get("/", include_in_schema=False)
    @app.get("/{path:path}", include_in_schema=False)
    def index(path: str) -> Any:
        react_index = os.path.join(static_folder_path, "react", "index.html")
        if os.path.exists(react_index):
            return FileResponse(react_index)
        return Response(status_code=404)

    return app
