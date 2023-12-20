from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer



# this serilizer is for creating the user when accessing: "http://127.0.0.1:8001/auth/jwt/create"
# here we overwrite the "UserCreateSerializer", we don;t need to have ViewSet (ViewSet is implemented by Djoser)
# after this you need to register in "settings.py"
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "username", "password", "email", "first_name", "last_name"]


# this serilizer is for getting the user info(after the client successfully once logged in and get the access-token)
# when accessing "http://127.0.0.1:8000/auth/users/me/" with modified header: {"Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMTU2MjQwLCJpYXQiOjE3MDMwNjk4NDAsImp0aSI6IjNkMzBiZmI1YTE5ZDRmNWQ4NzhhNGE1Y2UwYzVmMWQxIiwidXNlcl9pZCI6MX0.VyVLGg_jriYRdHw6y3q7c-L-Bh7p_aqUOOnhRgukThY"}
# after this you need to register in "settings.py"
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]