from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Users, UsersProfile
from .serializers import UsersSerializer, UsersProfileSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]


class UsersProfileViewSet(viewsets.ModelViewSet):
    queryset = UsersProfile.objects.all()
    serializer_class = UsersProfileSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Register new user with profile"""
    profile_data = {
        'profile_id': request.data.get('profile_id'),
        'f_name': request.data.get('f_name'),
        'l_name': request.data.get('l_name'),
        'user_type': request.data.get('user_type', 'customer'),
        'm_name': request.data.get('m_name'),
        'email': request.data.get('email'),
    }
    
    profile_serializer = UsersProfileSerializer(data=profile_data)
    if profile_serializer.is_valid():
        profile = profile_serializer.save()
        
        user_data = {
            'user_id': request.data.get('user_id'),
            'phone': request.data.get('phone'),
            'password': request.data.get('password'),
            'profile_id': profile.profile_id,
            'is_active': True,
        }
        
        user_serializer = UsersSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({
                'message': 'User created successfully',
                'user_id': user.user_id
            }, status=status.HTTP_201_CREATED)
        else:
            profile.delete()
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
