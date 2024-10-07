import jwt
from ginger.http import HttpResponseRedirect
from ginger.conf import settings
from src.references import GINGER_SOCIETY_IAM_FRONTEND_USERS


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = (
            GINGER_SOCIETY_IAM_FRONTEND_USERS + "/#" + settings.APP_ID + "/login"
        )

        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        print("access_token", access_token, request.path)

        if request.path.startswith("/handle-auth"):
            return self.get_response(request)

        # Check if access token or refresh token is missing
        if not access_token or not refresh_token:
            # Redirect to the external app's auth handler

            return HttpResponseRedirect(redirect_url)

        # Optional: Add JWT decoding for validation
        try:
            decoded_token = jwt.decode(
                access_token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            print("Decoded Claims:", decoded_token)
            request.decoded_jwt = decoded_token

        except Exception as e:
            print(e)
            return HttpResponseRedirect(redirect_url)
        except jwt.InvalidTokenError:
            return HttpResponseRedirect(redirect_url)

        # Proceed if everything is fine
        response = self.get_response(request)
        return response
