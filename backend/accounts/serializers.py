# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
# that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization,
# allowing parsed data to be converted back into complex types, after first validating the incoming data.
# The serializers in REST framework work very similarly to Django's Form and ModelForm classes. We provide a Serializer
# class which gives you a powerful, generic way to control the output of your responses, as well as a ModelSerializer
# class which provides a useful shortcut for creating serializers that deal with model instances and querysets.

from rest_framework import serializers
from .models import User
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class SignUpSerializer(serializers.ModelSerializer):
    """Serializer enabling unregistered users to sign up."""

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    new_password = serializers.CharField(
        label='Password',
        write_only=True,
        required=True,
        validators=[
            validate_password,
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$&+,:;=?@#|<>.^*()%!-]).*$',
                message='Password must contain an uppercase character, a lowercase character, a number and a special character.')
            ]
        )
    password_confirmation = serializers.CharField(
        label='Confirm password',
        write_only=True,
        required=True
        )

    class Meta:
        """Serializer options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'new_password', 'password_confirmation']


    def validate(self, attrs):
        """Validate the data and generate messages for any errors."""

        super().validate(attrs)
        if attrs['new_password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """Create a new user."""

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(self.validated_data['new_password'])
        user.save()

        return user
