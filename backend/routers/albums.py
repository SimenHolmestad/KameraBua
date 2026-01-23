from typing import Any, Iterable, List, Optional
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.camera_service import ImageCaptureError
from backend.album_service import album_service
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


def construct_album_api_router(
    albums_base_path: str,
    albums_dir: str,
    config: Config,
    forced_album_name: Optional[str] = None
) -> APIRouter:
    """Constructs route related to accessing the albums and adding new
    images to them using the camera module
    """
    album_api_router = APIRouter()

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

        On POST: Try to capture an image with the camera module and
        add the image to <album_name>.

        If the album does not exist, an error message is returned.
        """
        if forced_album_name and album_name != forced_album_name:
            return unaccessible_album_error_message()

        if not album_service.album_exists(albums_base_path, albums_dir, album_name):
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

        if not album_service.album_exists(albums_base_path, albums_dir, album_name):
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

        if not album_service.album_exists(albums_base_path, albums_dir, album_name):
            return error_response(
                status.HTTP_404_NOT_FOUND,
                f"No album with the name \"{album_name}\" exists"
            )

        relative_url = album_service.get_relative_url_of_last_image(
            albums_base_path,
            albums_dir,
            album_name
        )
        if not relative_url:
            return error_response(status.HTTP_404_NOT_FOUND, "album is empty")

        return {
            "last_image_url": create_static_url(request, relative_url)
        }

    def create_or_update_album(request_body: AlbumCreateRequest, request: Request) -> Any:
        if forced_album_name:
            return unaccessible_album_error_message()

        album_name = request_body.album_name
        album_service.get_or_create_album(albums_base_path, albums_dir, album_name)

        if request_body.description is not None:
            album_service.set_album_description(
                albums_base_path,
                albums_dir,
                album_name,
                request_body.description
            )

        return {
            "album_name": album_name,
            "album_url": request.url_for("album_info", album_name=album_name).path
        }

    def get_available_albums() -> Any:
        album_names = album_service.get_available_album_names(albums_base_path, albums_dir)
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
        relative_image_url, relative_thumbnail_url = album_service.capture_image_to_album(
            albums_base_path,
            albums_dir,
            album_name,
            config
        )
        return {
            "success": "Image successfully captured",
            "image_url": create_static_url(request, relative_image_url),
            "thumbnail_url": create_static_url(request, relative_thumbnail_url)
        }

    def get_album_information(request: Request, album_name: str) -> Any:
        description = album_service.get_album_description(albums_base_path, albums_dir, album_name)
        image_urls = album_service.get_relative_urls_of_all_images(
            albums_base_path,
            albums_dir,
            album_name
        )
        thumbnail_urls = album_service.get_relative_urls_of_all_thumbnails(
            albums_base_path,
            albums_dir,
            album_name
        )

        return {
            "album_name": album_name,
            "image_urls": create_static_url_list(request, image_urls),
            "thumbnail_urls": create_static_url_list(request, thumbnail_urls),
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
