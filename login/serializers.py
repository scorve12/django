from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['id', 'gender', 'age', 'email', 'username', 'password', 'last_login']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            gender=validated_data['gender'],
            age=validated_data.get('age'),
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
