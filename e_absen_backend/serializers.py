from rest_framework import serializers
from django.contrib.auth.models import User
from e_absen_backend.models.Employee import Employee
from rest_framework import generics, status
from django.http import JsonResponse
from .models.Employee import Employee
from .models.Location import Location
from .models.Role import Role
from .models.Shift import Shift

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name', 'is_active']

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    user_role = RoleSerializer(read_only=True)
    user_shift = ShiftSerializer(read_only=True)
    user_location = LocationSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'user_id', 'user_avatar', 'employee_name', 'is_active', 'user_role', 'user_payout', 'user_shift', 'user_location']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        employee = Employee.objects.create(user_id=user)
        return employee

    def update(self, instance, validated_data):
        instance.employee_name = validated_data.get('employee_name', instance.employee_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.user_payout = validated_data.get('user_payout', instance.user_payout)
        
        if 'user_avatar' in validated_data:
            instance.user_avatar = validated_data['user_avatar']
        
        if 'user_role' in validated_data:
            role_id = validated_data.pop('user_role')
            try:
                role_instance = Role.objects.get(role_id=role_id)
                instance.user_role = role_instance
            except Role.DoesNotExist:
                raise serializers.ValidationError("Invalid role ID")

        if 'user_shift' in validated_data:
            shift_id = validated_data.pop('user_shift')
            try:
                shift_instance = Shift.objects.get(id=shift_id)
                instance.user_shift = shift_instance
            except Shift.DoesNotExist:
                raise serializers.ValidationError("Invalid shift ID")

        if 'user_location' in validated_data:
            location_id = validated_data.pop('user_location')
            try:
                location_instance = Location.objects.get(id=location_id)
                instance.user_location = location_instance
            except Location.DoesNotExist:
                raise serializers.ValidationError("Invalid location ID")

        instance.save()
        return instance

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