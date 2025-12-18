from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Users
from .serializers import UsersSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # No authentication required for registration
def register(request):
    """Register new user and return JWT tokens"""
    # Validate incoming user data
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        # Create new user in database
        user = serializer.save()
        # Generate JWT tokens for immediate login after registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UsersSerializer(user).data,
            'refresh': str(refresh),  # Long-lived token for getting new access tokens
            'access': str(refresh.access_token),  # Short-lived token for API requests
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login with user_id/phone and password"""
    identifier = request.data.get('identifier')
    password = request.data.get('password')
    
    if not identifier or not password:
        return Response({'error': 'Identifier and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from django.db.models import Q
        user = Users.objects.get(Q(user_id=identifier) | Q(phone=identifier))
        
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UsersSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Users.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])  # Requires JWT authentication (default)
def verify_wallet_pin(request):
    """Verify wallet PIN for authenticated user before transactions"""
    # Get wallet ID and PIN from request
    wallet_id = request.data.get('wallet_id')
    pin = request.data.get('pin')
    
    # Validate required fields
    if not wallet_id or not pin:
        return Response({'error': 'Wallet ID and PIN required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from .models import Wallet
        # Ensure wallet belongs to authenticated user (security check)
        wallet = Wallet.objects.get(wallet_id=wallet_id, user=request.user)
        # Verify hashed PIN matches
        if wallet.check_pin(pin):
            return Response({'verified': True}, status=status.HTTP_200_OK)
        # PIN verification failed
        return Response({'error': 'Invalid PIN'}, status=status.HTTP_401_UNAUTHORIZED)
    except Wallet.DoesNotExist:
        # Wallet not found or doesn't belong to user
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
