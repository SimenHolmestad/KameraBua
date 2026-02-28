from typing import Any, Iterable, List, Optional
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.camera_service import CameraService, ImageCaptureError
from backend.album_service.album_service import AlbumService
from backend.core.config import Config


class AlbumCreateRequest(BaseModel):
    album_name: str
    description: Optional[str] = None


class AlbumCreatedResponse(BaseModel):
    album_name: str
    album_url: str


class AvailableAlbumsResponse(BaseModel):
    available_albums: List[str]
    forced_album: Optional[str] = None


class AlbumInfoResponse(BaseModel):
    album_name: str
    description: str
    image_urls: List[str]
    thumbnail_urls: List[str]


class AlbumCaptureResponse(BaseModel):
    success: str
    image_url: str
    thumbnail_url: str


class LastImageResponse(BaseModel):
    last_image_url: str


def construct_album_api_router(config: Config) -> APIRouter:
    """Constructs route related to accessing the albums and adding new
    images to them using the configured camera
    """
    album_api_router = APIRouter()
    album_service = AlbumService(config.albums, CameraService(config.camera))
    forced_album_name = config.albums.forced_album
    albums_dir = config.albums.albums_dir
    albums_url_prefix = _albums_url_prefix_from_dir(albums_dir)

    @album_api_router.get("/", response_model=AvailableAlbumsResponse)
    def available_albums() -> Any:
        """An endpoint for listing albums and create new albums.

        On GET: Return list of all available albums.

        On POST: Create a new album with the given album name if it
        does not already exists. If a description is given, set the
        description of the album.
        """

        return get_available_albums()

    @album_api_router.post("/", response_model=AlbumCreatedResponse)
    def create_album(request_body: AlbumCreateRequest, request: Request) -> Any:
        return create_or_update_album(request_body, request)

    @album_api_router.get(
        "/{album_name}",
        name="album_info",
        response_model=AlbumInfoResponse,
        operation_id="get_album_info"
    )
    def album_info(album_name: str, request: Request) -> Any:
        """An endpoint for listing images in an album or capture a new image
        to the album

        On GET: Returns a list of the image links for all images in
        <album_name>.

        On POST: Try to capture an image with the configured camera and
        add the image to <album_name>.

        If the album does not exist, an error message is returned.
        """
        if forced_album_name and album_name != forced_album_name:
            return unaccessible_album_error_message()

        if not album_service.album_exists(album_name):
            return error_response(
                status.HTTP_404_NOT_FOUND,
                f"No album with the name \"{album_name}\" exists"
            )

        return get_album_information(request, album_name)

    @album_api_router.post(
        "/{album_name}",
        response_model=AlbumCaptureResponse,
        operation_id="capture_image_to_album"
    )
    def capture_album_image(album_name: str, request: Request) -> Any:
        if forced_album_name and album_name != forced_album_name:
            return unaccessible_album_error_message()

        if not album_service.album_exists(album_name):
            return error_response(
                status.HTTP_404_NOT_FOUND,
                f"No album with the name \"{album_name}\" exists"
            )

        return try_capture_image_to_album(request, album_name)

    @album_api_router.get("/{album_name}/last_image", response_model=LastImageResponse)
    def last_image_for_album(album_name: str, request: Request) -> Any:
        """Returns the url of the last image captured to the specified
        album
        """
        if forced_album_name and album_name != forced_album_name:
            return unaccessible_album_error_message()

        if not album_service.album_exists(album_name):
            return error_response(
                status.HTTP_404_NOT_FOUND,
                f"No album with the name \"{album_name}\" exists"
            )

        image_name = album_service.get_last_image_name(album_name)
        if not image_name:
            return error_response(status.HTTP_404_NOT_FOUND, "album is empty")

        return {
            "last_image_url": create_static_url(
                request,
                _relative_url(albums_url_prefix, album_name, "images", image_name)
            )
        }

    def create_or_update_album(request_body: AlbumCreateRequest, request: Request) -> Any:
        if forced_album_name:
            return unaccessible_album_error_message()

        album_name = request_body.album_name
        album_service.get_or_create_album(album_name)

        if request_body.description is not None:
            album_service.set_album_description(album_name, request_body.description)

        return {
            "album_name": album_name,
            "album_url": request.url_for("album_info", album_name=album_name).path
        }

    def get_available_albums() -> Any:
        album_names = album_service.get_available_album_names()
        return {
            "available_albums": album_names,
            "forced_album": forced_album_name
        }

    def try_capture_image_to_album(request: Request, album_name: str) -> Any:
        try:
            return capture_image_to_album(request, album_name)
        except ImageCaptureError as e:
            return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def capture_image_to_album(request: Request, album_name: str) -> Any:
        album_service.capture_image_to_album(album_name)
        image_name = album_service.get_last_image_name(album_name) or ""
        thumbnail_name = album_service.get_last_thumbnail_name(album_name) or ""

        return {
            "success": "Image successfully captured",
            "image_url": create_static_url(
                request,
                _relative_url(albums_url_prefix, album_name, "images", image_name)
            ),
            "thumbnail_url": create_static_url(
                request,
                _relative_url(albums_url_prefix, album_name, "thumbnails", thumbnail_name)
            )
        }

    def get_album_information(request: Request, album_name: str) -> Any:
        description = album_service.get_album_description(album_name)
        image_names = album_service.get_image_names(album_name)
        thumbnail_names = album_service.get_thumbnail_names(album_name)

        return {
            "album_name": album_name,
            "image_urls": create_static_url_list(
                request,
                [
                    _relative_url(albums_url_prefix, album_name, "images", image_name)
                    for image_name in image_names
                ]
            ),
            "thumbnail_urls": create_static_url_list(
                request,
                [
                    _relative_url(albums_url_prefix, album_name, "thumbnails", thumbnail_name)
                    for thumbnail_name in thumbnail_names
                ]
            ),
            "description": description,
        }

    def create_static_url(request: Request, relative_url: str) -> str:
        return request.url_for("static", path=relative_url).path

    def create_static_url_list(request: Request, relative_url_list: Iterable[str]) -> List[str]:
        return list(map(lambda url: create_static_url(request, url), relative_url_list))

    def unaccessible_album_error_message() -> Any:
        return error_response(
            status.HTTP_403_FORBIDDEN,
            f"Illegal operation. The only accessible album is {forced_album_name}."
        )

    def error_response(status_code: int, message: str) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"error": message})

    return album_api_router


def _albums_url_prefix_from_dir(albums_dir: str) -> str:
    normalized = albums_dir.replace("\\", "/").rstrip("/")
    if not normalized:
        return ""
    return normalized.split("/")[-1]


def _relative_url(prefix: str, album_name: str, folder_name: str, filename: str) -> str:
    return "/".join(filter(None, [prefix, album_name, folder_name, filename]))
