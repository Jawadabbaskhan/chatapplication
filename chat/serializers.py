from rest_framework import serializers
from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):  # Changed to ModelSerializer
    senderDetails = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['user']

    def get_senderDetails(self,obj):
        user = {
            'id':obj.user.id,
            'userName': obj.user.username,
            'firstName':obj.user.first_name,
            'lastName': obj.user.last_name,
            'userEmail': obj.user.email
        }
        return user