from IAMService_client.IAMService.api_client import ApiClient
from ginger.http import HttpResponseRedirect
from ginger.shortcuts import redirect
import certifi
from ginger.http import HttpResponse
from ginger.shortcuts import redirect


from IAMService_client.IAMService import (
    RefreshTokenRequest,
    Configuration,
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

    conf = Configuration(
        host="https://api-staging.gingersociety.org/iam",
        ssl_ca_cert=certifi.where(),
        api_key={
            "BearerAuth": access_token
        },  # Set the access token with 'BearerAuth' identifier
        api_key_prefix={"BearerAuth": "Bearer"},
    )

    print(conf)

    api_client = ApiClient(configuration=conf)

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

    # Update the 'access_token' cookie with the new token
    http_response.set_cookie("access_token", "")
    # Update the 'access_token' cookie with the new token
    http_response.set_cookie("refresh_token", "")
    return http_response
