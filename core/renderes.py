from typing import Any, Mapping, Optional, cast

from rest_framework.renderers import JSONRenderer


class GlobalResponseRenderer(JSONRenderer):
    """
    Global renderer that wraps all API responses in a unified structure:
    {
        "code": 0 | 1,
        "message": "Success" | "Error",
        "data": {...} or null,
        "errors": {...} or null
    }
    """

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> bytes:
        response = None
        if renderer_context is not None:
            response = renderer_context.get("response")

        result: dict[str, Any] = {
            "result_code": 0,
            "message": "Success",
            "data": data,
            "errors": None,
        }

        if response is not None and getattr(response, "status_code", 200) >= 400:
            result["result_code"] = 1
            result["message"] = "Error"
            result["data"] = None
            result["errors"] = data

        # cast ensures type compatibility with DRF stub return (Any → bytes)
        return cast(
            bytes, super().render(result, accepted_media_type, renderer_context)
        )
