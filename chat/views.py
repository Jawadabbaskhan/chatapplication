from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message
from chat.serializers import MessageSerializer


@api_view(['GET'])
def getMessages(request, course):
    print("course",course)
    all_messages = Message.objects.filter(course=course)
    print(all_messages)
    serializer = MessageSerializer(all_messages, many=True)
    print("-----------------------------")
    print(serializer.data)
    return Response(reversed(serializer.data), status=status.HTTP_200_OK)
