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
        user = request.github.client.get('https://api.github.com/user').json()
        repos = request.github.client.get(user['repos_url']).json()
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
