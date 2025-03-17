from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Incluye el rol del usuario en el JWT."""
    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
        token['role'] = user.role  # ✅ Agrega el rol al JWT
        token["username"] = user.username
        token["is_staff"] = user.is_staff
        
        return token
