from rest_framework import serializers
from .models import CustomUser
from .models import Trip

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
    
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'content', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']  # Set these fields as read-only

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
