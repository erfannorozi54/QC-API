"""Custom authentication class for camera"""
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication


class ConstantTokenAuthentication(TokenAuthentication):
    """Custom authentication class that checks for a constant token in the headers."""

    def authenticate(self, request):
        # Fetch the constant token from headers
        constant_token = request.headers.get('X-CONSTANT-TOKEN')
        if request.method == 'POST':
            # Check if the token matches the constant token
            if constant_token != '#camera#spesific#token#':
                raise AuthenticationFailed('Invalid or missing constant token')

            # Return None to indicate that no user is attached to this authentication
            # since we are using a constant token, we are not dealing with user-specific tokens.
            return (None, None)
        else:
            self.super().authenticate()
