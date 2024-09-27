from rest_framework import generics, status
from rest_framework.response import Response
from e_absen_backend.models.serializers import UserIdSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserIdSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()

        return Response({
            'user': {
                'username': user_profile.user_id.username,
                'email': user_profile.user_id.email,
                'user_name': user_profile.user_name,
            },
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)