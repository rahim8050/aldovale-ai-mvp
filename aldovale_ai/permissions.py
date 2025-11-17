import logging
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from django.conf import settings
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError

logger = logging.getLogger(__name__)


class HasValidAPIKey(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        auth_header = request.headers.get("Authorization", "")
        logger.debug(f"[Auth Debug] Authorization header: {auth_header}")

        if not auth_header.startswith("Bearer "):
            logger.warning("[Auth Debug] Missing or malformed Authorization header.")
            return False

        token = auth_header[len("Bearer ") :].strip()
        logger.debug(f"[Auth Debug] Extracted token: {token}")

        jwt_secret = getattr(settings, "JWT_SECRET_KEY", None)
        if not jwt_secret:
            logger.error("[Auth Debug] JWT_SECRET_KEY not set in settings.")
            return False  # Deny if no secret configured

        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            logger.debug(f"[Auth Debug] JWT payload decoded: {payload}")
        except ExpiredSignatureError:
            logger.warning("[Auth Debug] JWT token expired.")
            return False
        except InvalidTokenError as e:
            logger.warning(f"[Auth Debug] Invalid JWT token: {e}")
            return False
        except Exception as e:
            logger.error(f"[Auth Debug] Unexpected JWT decode error: {e}")
            return False

        if payload.get("sub") != "service-api":
            logger.warning(f"[Auth Debug] Invalid 'sub' claim: {payload.get('sub')}")
            return False

        logger.debug("[Auth Debug] Authorization granted.")
        return True
