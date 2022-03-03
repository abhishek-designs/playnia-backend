from rest_framework import serializers
from .models import UserLobby
from django.utils.translation import gettext as _

class UserLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLobby
        fields = '__all__'
        extra_kwargs = {'users': { 'read_only': True }, 'created_on': { 'read_only': True }, 'created_by': { 'read_only': True }}
    
    def create(self, validated_data):
        """
            Create a new lobby and save it
        """
        name = validated_data.get('name')
        img = validated_data.get('img')
        thumbnail = validated_data.get('thumbnail')
        created_by = self.context.get('user')
        # Now the save the data to the database
        try:
            lobby = UserLobby(name=name, img=img, thumbnail=thumbnail, created_by=created_by)
            lobby.save()
            return lobby
        except:
            raise serializers.ValidationError(_('Error while creating lobby'))
    
    # def update(self, instance, validated_data):
    #     """
    #         Update the lobby and add the user
    #     """
    #     follower_count = validated_data.get('follower_count')
    #     user = self.context.get('user')
    #     print(follower_count, user)
    #     return instance
    
    def to_representation(self, instance):
        """
            Update followers count
        """
        representation = super().to_representation(instance)
        print(representation, self.context.get('followers_count'))
        return representation
        
        
        