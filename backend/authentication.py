from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Users, AuthToken
from .serializers import UsersSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """Verify auth token for remember me"""
    auth_token = request.data.get('auth_token')
    user_id = request.data.get('user_id')
    
    if not auth_token or not user_id:
        return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = AuthToken.objects.select_related('user__profile_id').get(token=auth_token, user__user_id=user_id)
        if token.user.profile_status.upper() == 'ACTIVE':
            return Response({
                'valid': True,
                'user_id': token.user.user_id,
                'name': f"{token.user.profile_id.f_name} {token.user.profile_id.l_name}",
                'phone': token.user.phone
            }, status=status.HTTP_200_OK)
        return Response({'valid': False}, status=status.HTTP_403_FORBIDDEN)
    except AuthToken.DoesNotExist:
        return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)


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
        user = Users.objects.select_related('profile_id').get(Q(user_id=identifier) | Q(phone=identifier))
        
        if user.profile_status.upper() != 'ACTIVE':
            return Response({'error': 'Account is not active'}, status=status.HTTP_403_FORBIDDEN)
        
        if user.check_password(password):
            AuthToken.objects.filter(user=user).delete()
            token = AuthToken.objects.create(token=AuthToken.generate_token(), user=user)
            
            return Response({
                'auth_token': token.token,
                'user_id': user.user_id,
                'name': f"{user.profile_id.f_name} {user.profile_id.l_name}",
                'phone': user.phone
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
