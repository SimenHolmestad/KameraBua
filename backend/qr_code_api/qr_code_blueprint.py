from typing import Any
from flask import Blueprint, jsonify, url_for


def construct_qr_code_api_blueprint(qr_code_handler: Any) -> Blueprint:
    """Construct routes related to accessing qr-codes."""
    qr_code_api_blueprint = Blueprint("qr", __name__)

    @qr_code_api_blueprint.route("/", methods=["GET"])
    def get_qr_codes() -> Any:
        qr_codes = qr_code_handler.get_qr_codes()
        qr_code_dicts = list(map(
            lambda qr_code: {
                "name": qr_code.get_name(),
                "information": qr_code.get_information_text(),
                "url": url_for("static", filename=qr_code.get_relative_url())
            },
            qr_codes
        ))

        return jsonify({
            "qr_codes": qr_code_dicts
        })

    return qr_code_api_blueprint
