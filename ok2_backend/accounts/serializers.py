from rest_framework import serializers

from accounts.models import OkUser


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkUser
        fields = ['email', 'password', ]

        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        email = data.get('email')


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = OkUser
        fields = ['email', 'first_name', 'last_name',
                  'password', 'confirm_password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        print(self)
        user = OkUser(
            email=self.validated_data['email'],
            username=self.validated_data['email']
        )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        user.set_password(password)
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.role = self.validated_data['role']
        user.save()
        return user
