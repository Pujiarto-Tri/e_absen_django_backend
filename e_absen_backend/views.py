from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationView(generics.CreateAPIView):
    # from e_absen_backend.serializers import UserIdSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()

        return Response({
            'user': {
                'email': user_profile.user_id.email,
            },
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'name': user.user_id.name if hasattr(user, 'user_id') else None,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
