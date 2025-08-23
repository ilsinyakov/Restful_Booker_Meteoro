import json

import allure
import requests
from allure_commons.types import AttachmentType


def attach_request_response(response: requests.Response) -> None:
    # Request
    request = response.request
    try:
        request_body = json.dumps(json.loads(request.body), indent=2) if request.body else ""
        request_attachment_type = AttachmentType.JSON
    except Exception:
        request_body = str(request.body or "")
        request_attachment_type = AttachmentType.TEXT

    allure.attach(
        f"{request.method} {request.url}",
        name="Request",
        attachment_type=AttachmentType.TEXT,
    )
    allure.attach(
        json.dumps(dict(request.headers), indent=2),
        name="Request headers",
        attachment_type=AttachmentType.JSON,
    )
    if request_body:
        allure.attach(request_body, name="Request body", attachment_type=request_attachment_type)

    # Response
    try:
        response_body = json.dumps(response.json(), indent=2)
        response_attachment_type = AttachmentType.JSON
    except Exception:
        response_body = response.text
        response_attachment_type = AttachmentType.TEXT

    allure.attach(
        f"{response.status_code} {response.reason}",
        name="Response",
        attachment_type=AttachmentType.TEXT,
    )
    allure.attach(json.dumps(dict(response.headers), indent=2),
                  name="Response headers",
                  attachment_type=AttachmentType.JSON,
    )
    allure.attach(response_body, name="Response body", attachment_type=response_attachment_type)
