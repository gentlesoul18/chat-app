from rest_framework import serializers
from api.models import User, ChatMessage, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','user', 'bio', 'avatar', 'verified']

class MessageSerializer(serializers.ModelSerializer):
    receiver_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id','user', 'sender','sender_profile', 'receiver','receiver_profile', 'message', 'is_read', 'date']