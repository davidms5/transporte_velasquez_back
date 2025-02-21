from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Incluye el rol del usuario en el JWT."""
    def get_token(self, user):
        token = super().get_token(user)
        token['role'] = user.role  # ✅ Agrega el rol al JWT
        return token
