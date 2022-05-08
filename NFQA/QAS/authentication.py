import jwt
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.serializers import jwt_decode_handler
from rest_framework_jwt.utils import jwt_get_username_from_payload_handler
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class JWTAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):

        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            raise AuthenticationFailed('User Authentication failed. A token is required')

        try:
            auth = auth.split(' ')[-1].strip()
            payload = jwt_decode_handler(auth)

        # 出现jwt解析异常，直接抛出异常，代表非法用户，也可以返回None，作为游客处理
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Expired token')
        except jwt.DecodeError:
            raise AuthenticationFailed('Illegal token')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user = self.authenticate_credentials(payload)
        return user, auth

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id, phone and email.
        """

        User = get_user_model()
        username = jwt_get_username_from_payload_handler(payload)

        if not username:
            raise AuthenticationFailed('Invalid payload')

        try:
            user = User.objects.get_by_natural_key(username)

        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid signature')

        if not user.is_active:
            raise AuthenticationFailed('User account is disabled')

        return user
