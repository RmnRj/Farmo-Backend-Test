"""
Authentication service module
Handles login and token verification
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from backend.models import Users, AuthToken


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login with user_id/phone and password
    
    Validates credentials and checks if profile_status is ACTIVE.
    Generates and returns authentication token on success.
    
    Request data:
    - identifier: user_id or phone
    - password: user password
    
    Returns:
    - 200: Login successful with auth_token
    - 400: Missing credentials
    - 401: Invalid credentials
    - 403: Account not active
    """
    identifier = request.data.get('identifier')
    password = request.data.get('password')
    is_admin = request.data.get('is_admin', False)
    device_info = request.data.get('device_info', '')
    
    if not identifier or not password:
        return Response({'error': 'Identifier and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from django.db.models import Q
        # Find user by user_id or phone
        user = Users.objects.select_related('profile_id').get(Q(user_id=identifier) | Q(phone=identifier))
        
        # Check if account is active
        if user.profile_status.upper() != 'ACTIVE':
            return Response({'error': 'Account is not active'}, status=status.HTTP_403_FORBIDDEN)
        
        # Verify password
        if user.check_password(password):
            # Delete old tokens and create new one
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


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """Verify auth token for remember me functionality
    
    Checks if provided token is valid and associated with active user.
    
    Request data:
    - auth_token: Authentication token
    - user_id: User identifier
    
    Returns:
    - 200: Token valid with user details
    - 400: Missing parameters
    - 401: Invalid token
    - 403: Account not active
    """
    auth_token = request.data.get('auth_token')
    user_id = request.data.get('user_id')
    
    if not auth_token or not user_id:
        return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Verify token exists and belongs to user
        token = AuthToken.objects.select_related('user__profile_id').get(token=auth_token, user__user_id=user_id)
        
        # Check if account is still active
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
def verify_wallet_pin(request):
    """Verify wallet PIN for authenticated user before transactions
    
    Request data:
    - wallet_id: Wallet identifier
    - pin: 4-digit PIN
    
    Returns:
    - 200: PIN verified successfully
    - 400: Missing parameters
    - 401: Invalid PIN
    - 404: Wallet not found
    """
    wallet_id = request.data.get('wallet_id')
    pin = request.data.get('pin')
    
    if not wallet_id or not pin:
        return Response({'error': 'Wallet ID and PIN required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from backend.models import Wallet
        wallet = Wallet.objects.get(wallet_id=wallet_id, user=request.user)
        if wallet.check_pin(pin):
            return Response({'verified': True}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid PIN'}, status=status.HTTP_401_UNAUTHORIZED)
    except Wallet.DoesNotExist:
        return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)

