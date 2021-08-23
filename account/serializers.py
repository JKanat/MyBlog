from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import MyUser

from .utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=6, write_only=True)
    password_confirm = serializers.CharField(max_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validate_data):
        password = validate_data.get('password')
        password_confirm = validate_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validate_data

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code,
                             status='register')
        return user
    # """This function is called when self.save() method is called """


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                message = 'Unable to login in with provided credentials'
                raise serializers.ValidationError(message, code="authorization")
        else:
            message = "Must include 'email' and 'password'."
            raise serializers.ValidationError(message, code="authorization")

        attrs['user'] = user
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=25,
                                            required=True)
    password = serializers.CharField(min_length=8,
                                     required=True)
    password_confirmation = serializers.CharField(min_length=8,
                                                  required=True)

    def validate_email(self, email):
        print(email)
        if not MyUser.objects.filter(email=email):
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_activation_code(self, act_code):
        if not MyUser.objects.filter(activation_code=act_code,
                                     is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return act_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_conf = attrs.pop('password_confirmation')
        if password != password_conf:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get(email=email,
                                      activation_code=activation_code,
                                      is_active=False)
        except MyUser.DoesMotexist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user
