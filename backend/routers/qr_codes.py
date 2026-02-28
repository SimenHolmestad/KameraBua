from typing import Any, Iterable, List, Mapping
from fastapi import APIRouter, Request
from pydantic import BaseModel


class QrCodeResponse(BaseModel):
    name: str
    information: str
    url: str


class QrCodesResponse(BaseModel):
    qr_codes: List[QrCodeResponse]


def construct_qr_code_api_router(qr_codes: Iterable[Mapping[str, str]]) -> APIRouter:
    """Construct routes related to accessing qr-codes."""
    qr_code_api_router = APIRouter()

    @qr_code_api_router.get("/", response_model=QrCodesResponse)
    def get_qr_codes(request: Request) -> Any:
        qr_code_dicts = [
            {
                "name": qr_code["name"],
                "information": qr_code["information"],
                "url": request.url_for("static", path=qr_code["relative_url"]).path
            }
            for qr_code in qr_codes
        ]

        return {
            "qr_codes": qr_code_dicts
        }

    return qr_code_api_router
