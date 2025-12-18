from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Users, UsersProfile
from .serializers import UsersSerializer, UsersProfileSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on Users model
    Requires authentication for all operations
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]


class UsersProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on UsersProfile model
    Requires authentication for all operations
    """
    queryset = UsersProfile.objects.all()
    serializer_class = UsersProfileSerializer
    permission_classes = [IsAuthenticated]
