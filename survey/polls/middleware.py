import jwt


class Profile:
    def __init__(self, payload):
        self.user_id = payload['user_id']


class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # قبل از پردازش view
        if '/api/' not in request.path:
            return self.get_response(request)

        jwt_token = request.headers.get('authorization', None)
        jwt_token = str.replace(str(jwt_token), 'Bearer ', '')
        payload = jwt.decode(jwt_token, options={"verify_signature": False})
        request.profile = Profile(payload)
        response = self.get_response(request)
        # بعد از پردازش view
        return response
