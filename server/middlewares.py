import jwt
from gingerdj.http import HttpResponseRedirect
from gingerdj.conf import settings
from src.references import GINGER_SOCIETY_IAM_FRONTEND_USERS


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = (
            GINGER_SOCIETY_IAM_FRONTEND_USERS + "/#" + settings.APP_ID + "/login"
        )

        # Retrieve tokens from headers or cookies
        access_token = request.COOKIES.get(
            "access_token"
        ) or self.get_token_from_header(request)
        refresh_token = request.COOKIES.get("refresh_token")

        print("access_token", access_token, request.path)

        if request.path.startswith("/handle-auth") or request.path.startswith(
            "/swagger"
        ):
            return self.get_response(request)

        # Check if access token or refresh token is missing
        if not access_token and not refresh_token:
            return HttpResponseRedirect(redirect_url)

        # Try to decode the JWT token
        try:
            # Decode the token after removing "Bearer " if present
            decoded_token = jwt.decode(
                access_token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            print("Decoded Claims:", decoded_token)
            request.decoded_jwt = decoded_token

        except jwt.InvalidTokenError:
            return HttpResponseRedirect(redirect_url)
        except Exception as e:
            print(f"JWT decoding error: {e}")
            return HttpResponseRedirect(redirect_url)

        # Proceed if everything is fine
        response = self.get_response(request)
        return response

    def get_token_from_header(self, request):
        """
        Retrieves the access token from either the 'Authorization' or 'X-API-Authorization' headers.
        Both headers should follow the 'Bearer' schema.
        """
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        api_auth_header = request.headers.get("X-API-Authorization")

        if auth_header:
            return auth_header.replace("Bearer ", "")  # Remove "Bearer " prefix
        elif api_auth_header:
            return api_auth_header.replace("Bearer ", "")  # Remove "Bearer " prefix

        return None
