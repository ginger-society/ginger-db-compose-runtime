from ginger.http import HttpResponseRedirect
from ginger.shortcuts import redirect


def handle_auth(request, access_token, refresh_token):
    # Check if tokens are provided in the URL path
    if access_token and refresh_token:
        # Set cookies with tokens
        response = HttpResponseRedirect("/admin")
        response.set_cookie("access_token", access_token)
        response.set_cookie("refresh_token", refresh_token)
        return response
    else:
        # If tokens are missing, redirect to error or login page
        return redirect("/error")  # Can redirect to a custom error page
