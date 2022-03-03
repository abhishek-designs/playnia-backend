from rest_framework import serializers
from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password', 'bio', 'followers', 'following', 'total_questions', 'total_answers', 'profile_pic']
        extra_kwargs = {'id': {'read_only': True} }

    def create(self, data):
        """
            This method will trigger when new user is going to create or save
        """
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if first_name is not None and last_name is not None and email is not None and password is not None:
            # Create the user and save
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            # Hash the password
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError(_('Credentials should not be blank'))   

    def update(self, instance, validated_data):
        """
            This method will trigger when new user is going to update
        """
        # return the instance data if user doesn't specify the whole data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # Updating bio
        instance.bio = validated_data.get('bio', instance.bio)
        # Updating followers
        if validated_data.get('followers') == 0:
            instance.followers = 0
        else:
            instance.followers += validated_data.get('followers', 0)
        # Updating following
        if validated_data.get('following') == 0:
            instance.following = 0
        else:
            instance.following += validated_data.get('following', 0)
        # Updating profile pic
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        print('profile pic uploaded')
        # Save the data to database
        instance.save()
        return validated_data

    def validate_password(self, value):
        """
            Validate the password as well on registering user
        """
        re_pattern = '(?=(.*[A-Z]))(?=(.*[a-z]))(?=(.*[0-9]))(?=(.*[*%@#&\\^_])).{6,}'
        # Validate the password with regex
        if value and not re.match(re_pattern, value):
            raise serializers.ValidationError(_('Sorry password is not compatible please check'))
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150)

    def validate(self, data):
        """
            This method will trigger when we validate the credentials
        """
        email = data.get('email')
        password = data.get('password')
        
        if email is not None and password is not None:
            # Now checking the user
            user = authenticate(email=email, password=password)
            if user is not None:
                # User is authenticated
                return user
            else:
                raise serializers.ValidationError(_('Your email or password is invalid'))
        else:
            raise serializers.ValidationError(_('Please give the credentials'))
