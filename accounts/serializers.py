from rest_framework import serializers
from .models import SupervisorProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = SupervisorProfile
        fields = [
            'username', 'email', 'password',
            'phone_number', 'organization', 'request_message',
        ]

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = SupervisorProfile(**validated_data, status='PENDING')
        user.set_password(password)
        user.save()
        return user


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorProfile
        fields = [
            'username', 'email', 'status',
            'assigned_patient_mode', 'last_connected', 'approved_at',
        ]
        read_only_fields = fields


class TokenVerifySerializer(serializers.Serializer):
    is_valid = serializers.BooleanField()
    username = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    assigned_patient_mode = serializers.CharField(required=False)
