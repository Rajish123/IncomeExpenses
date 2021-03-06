from rest_framework import serializers

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 15, min_length = 6, write_only = True)

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError(
            'The username should contain alphanumeric characters'
            )
        return attrs

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

# in email verify end-point no parameters[fields] to verify email.
# so needed exterior class  that exposes field to view
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)

    class Meta:
        model = User
        fields = ['token']
