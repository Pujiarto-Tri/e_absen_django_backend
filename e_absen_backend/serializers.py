from rest_framework import serializers
from django.contrib.auth.models import User
from e_absen_backend.models.model_user import Employee
from rest_framework import generics, status
from django.http import JsonResponse

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'user_id', 'employee_name', 'user_avatar', 'user_role', 'user_payout', 'user_shift', 'user_location')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        user_id = Employee.objects.create(user_id=user, **validated_data)
        return user_id

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            return JsonResponse({
                'user': {
                    'email': user_profile.user.email,  # Access user attribute correctly
                },
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)