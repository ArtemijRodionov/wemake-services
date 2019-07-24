from test_assignment.auth_session import GithubSession


class GithubOauthMiddleware:

    Session = GithubSession

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.github = self.Session(request)
        return self.get_response(request)
