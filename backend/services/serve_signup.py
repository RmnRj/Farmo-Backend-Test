"""
Signup service module
Handles multi-stage user registration process
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.models import Users, UsersProfile
from backend.serializers import UsersSerializer, UsersProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Multi-stage user registration endpoint
    
    Creates both UsersProfile and Users records in a single transaction.
    Profile ID is auto-generated using UUID.
    
    Request data includes:
    - Basic info: user_id, f_name, l_name, m_name, user_type, password
    - Address: province, district, ward, tole
    - Contact: phone, phone02, email, whatsapp, facebook
    
    Returns:
    - 201: User created successfully with user_id
    - 400: Validation errors
    """
    import uuid
    
    # Auto-generate unique profile ID (format: P + 8 random uppercase hex chars)
    profile_id = f"P{uuid.uuid4().hex[:8].upper()}"
    
    # Prepare profile data from multi-stage form
    profile_data = {
        'profile_id': profile_id,
        'f_name': request.data.get('f_name'),  # First name (required)
        'l_name': request.data.get('l_name'),  # Last name (required)
        'user_type': request.data.get('user_type', 'customer'),  # Default: customer
        'm_name': request.data.get('m_name'),  # Middle name (optional)
        'email': request.data.get('email'),  # Email (optional)
        'province': request.data.get('province'),  # Address fields (optional)
        'district': request.data.get('district'),
        'ward': request.data.get('ward'),
        'tole': request.data.get('tole'),
        'phone02': request.data.get('phone02'),  # Secondary phone (optional)
        'whatsapp': request.data.get('whatsapp'),  # WhatsApp number (optional)
        'facebook': request.data.get('facebook'),  # Facebook profile (optional)
    }
    
    # Validate and create profile
    profile_serializer = UsersProfileSerializer(data=profile_data)
    if profile_serializer.is_valid():
        profile = profile_serializer.save()
        
        # Prepare user data linked to created profile
        user_data = {
            'user_id': request.data.get('user_id'),  # Unique user identifier
            'phone': request.data.get('phone'),  # Primary phone (required)
            'password': request.data.get('password'),  # Will be hashed by serializer
            'profile_id': profile.profile_id,  # Link to created profile
            'is_active': True,  # Activate user immediately
        }
        
        # Validate and create user
        user_serializer = UsersSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({
                'message': 'User created successfully',
                'user_id': user.user_id
            }, status=status.HTTP_201_CREATED)
        else:
            # Rollback: Delete profile if user creation fails
            profile.delete()
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
