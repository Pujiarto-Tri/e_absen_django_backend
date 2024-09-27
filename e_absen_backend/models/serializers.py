from rest_framework import serializers
from django.contrib.auth.models import User
from e_absen_backend.models.model_user import User_Id
from e_absen_backend.models.model_role import Role
from e_absen_backend.models.model_shift_time import Shift
from e_absen_backend.models.model_location import Location

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserIdSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    user_role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)
    user_shift = serializers.PrimaryKeyRelatedField(queryset=Shift.objects.all(), required=False, allow_null=True)
    user_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User_Id
        fields = ['user_id', 'user_avatar', 'user_name', 'is_active', 'user_role', 'user_payout', 'user_shift', 'user_location']
        extra_kwargs = {
            'user_name': {'required': False, 'allow_null': True},
            'user_payout': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user_id')
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data, password=password)

        user_profile = User_Id.objects.create(
            user_id=user,
            **validated_data
        )
        return user_profile