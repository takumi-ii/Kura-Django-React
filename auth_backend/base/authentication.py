from rest_framework_simplejwt.authentication import JWTAuthentication


class CookiesJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that sets cookies for access and refresh tokens.
    """
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None  # ← トークンなしなら未認証扱い（強制401にならない）

        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except Exception:
            # 無効なトークンは未認証としてスルー（401出さない）
            return None