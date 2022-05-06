import jwt
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.serializers import jwt_decode_handler
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_get_username_from_payload_handler


class MyJWTAuthenticate(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):

        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            raise AuthenticationFailed('User Authentication failed. A token is required')

        try:
            auth = auth.split(' ')[-1].strip()

            payload = jwt_decode_handler(auth)

        # 出现jwt解析异常，直接抛出异常，代表非法用户，也可以返回None，作为游客处理
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('The token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Illegal token')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user = self.authenticate_credentials(payload)
        return user, auth

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """

        User = get_user_model()
        username = jwt_get_username_from_payload_handler(payload)

        if not username:
            msg = 'Invalid payload.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
            # user = User.objects.get(username=username)
        except User.DoesNotExist:
            msg = 'Invalid signature.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'User account is disabled.'
            raise exceptions.AuthenticationFailed(msg)

        return user
