from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from oauthlib.oauth2.rfc6749.errors import MissingCodeError, MismatchingStateError


def index(request):
    if not request.github.authorized:
        context = {
            'username': 'Anonym',
        }
    else:
        response = request.github.client.get('https://api.github.com/user')
        response.raise_for_status()
        user = response.json()

        response = request.github.client.get(user['repos_url'])
        response.raise_for_status()
        repos = response.json()

        context = {
            'username': user['login'],
            'avatar_url': user['avatar_url'],
            'repos': repos,
        }

    return render(request, 'index.html', context)


def login(request):
    """"Redirect an user to request its GitHub identity."""
    return redirect(request.github.auth_url())


def authorize(request):
    """Authorize an access token."""
    try:
        request.github.update_token()
    except (MissingCodeError, MismatchingStateError):
        return HttpResponseForbidden()
    return redirect(reverse('index'))
