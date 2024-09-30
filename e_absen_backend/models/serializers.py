from rest_framework import serializers
from django.contrib.auth.models import User
from e_absen_backend.models.model_user import User_Id
from e_absen_backend.models.model_role import Role
from e_absen_backend.models.model_shift_time import Shift
from e_absen_backend.models.model_location import Location

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        # Ensure passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove the password2 field from validated_data
        password = validated_data.pop('password')
        user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'], password=password)
        return user


class UserIdSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    user_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)
    user_shift = serializers.PrimaryKeyRelatedField(queryset=Shift.objects.all(), required=False, allow_null=True)
    user_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User_Id
        fields = ['user_id', 'user_avatar', 'name', 'is_active', 'user_role', 'user_payout', 'user_shift', 'user_location']
        extra_kwargs = {
            'name': {'required': False, 'allow_null': True},
            'user_payout': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user_id')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        user_profile = User_Id.objects.create(
            user_id=user,
            **validated_data
        )
        return user_profile
