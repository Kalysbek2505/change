from rest_framework import serializers
from django.contrib.auth import get_user_model
from .tasks import send_activation_code
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']


    def valdate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким адресом электронной почты уже существует')


    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Пароль не совпадает')

        return attrs 

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)

    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.set_activation_code()