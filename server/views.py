from IAMService_client.IAMService.api_client import ApiClient
from IAMService_client.IAMService.config_utils import get_configuration
from gingerdj.http import HttpResponseRedirect
from gingerdj.shortcuts import redirect
from gingerdj.http import HttpResponse, JsonResponse
from gingerdj.shortcuts import redirect


from IAMService_client.IAMService import (
    RefreshTokenRequest,
    DefaultApi,
)


def handle_auth(request, access_token, refresh_token):
    # Check if tokens are provided in the URL path
    if access_token and refresh_token:
        # Set cookies with tokens
        response = HttpResponseRedirect("/admin/src")
        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)
        return response
    else:
        # If tokens are missing, redirect to error or login page
        return redirect("/error")  # Can redirect to a custom error page


def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")
    access_token = request.COOKIES.get("access_token")
    refresh_token_request = RefreshTokenRequest(refresh_token=refresh_token)

    api_client = ApiClient(configuration=get_configuration(access_token))

    api_instance = DefaultApi(api_client)

    response = api_instance.identity_refresh_token(
        refresh_token_request=refresh_token_request
    )
    new_access_token = response.access_token  # Adjust this based on actual API response

    # Create an HTTP response object
    http_response = HttpResponse(status=200)  # Basic OK response

    # Update the 'access_token' cookie with the new token
    http_response.set_cookie("access_token", new_access_token)

    # Return the response with the updated cookie
    return http_response


def clear_session(request):
    # Clear all cookies
    http_response = HttpResponse(status=200)  # Basic OK response

    # Clear cookies for the current domain and path
    http_response.set_cookie("access_token", "", max_age=0, path="/")
    http_response.set_cookie("refresh_token", "", max_age=0, path="/")
    return http_response


def get_additional_info(request):
    # Access the decoded JWT claims from the request
    if 'decoded_jwt' in request:
        decoded_jwt = request.decoded_jwt

        # Extract the "sub" claim (usually used as the user's email or unique ID)
        email = decoded_jwt.get("sub", "Unknown")

        # Return the email in the JSON response
        return JsonResponse({"email": email}, status=200)
    else:
        return JsonResponse({} , status=404)


def index(request):
    """Redirects the root URL to /admin/src."""
    return HttpResponseRedirect("/admin/src")
