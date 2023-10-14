from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Q

from rest_framework import generics, views, status
from rest_framework.response import Response

from api.serializers import MessageSerializer, ProfileSerializer
from api.models import ChatMessage, User, Profile
# get all messages
class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        messages = ChatMessage.objects.filter(
            id__in = Subquery(
                User.objects.filter(
                    Q(sender__receiver = user_id) | Q(receiver__sender = user_id)
                ).distinct().annotate(
                    last_msg = Subquery(
                        ChatMessage.objects.filter(
                            Q(sender=OuterRef('id'), receiver=user_id) | Q(receiver=OuterRef('id'), sender= user_id)
                        ).order_by("-id").values_list("id", flat=True)
                        
                    )
                ).values_list("last_msg", flat=True).order_by("-id")
            )
        ).order_by("-id")

        return messages
    

class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']

        messages = ChatMessage.objects.filter(
            sender__in = ['sender_id', 'receiver_id'],
            receiver__in = ['sender_id', 'receiver_id']
        )

        return messages
    

class ProfileDetail(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer


class Search(generics.ListAPIView):
    

    def get_serializer_class(self):
        if Profile.objects.filter(user__username= self.kwargs['search']).exists():
            return ProfileSerializer
        return MessageSerializer
        
    def get_queryset(self):
        if Profile.objects.filter(user__username= self.kwargs['search']).exists():
            return Profile.objects.all()
        return ChatMessage.objects.all()
    
    def list(self, request, *args, **kwargs):
        search = self.kwargs['search']
        user = self.request.user
        profile_exists = Profile.objects.filter(user__username= search).exists()
        message_exists = ChatMessage.objects.filter(message__icontains=search).exists()
        if not profile_exists and not message_exists:
            return Response({
                "details": "Result not found!"
            }, status=status.HTTP_404_NOT_FOUND)

        if Profile.objects.filter(user__username= search).exists():
            result = Profile.objects.filter(user__username__icontains=search).filter(user=user)
            serializer = self.get_serializer(result, many = True)
            return Response(serializer.data)
        
        result = ChatMessage.objects.filter(message__icontains=search).filter(user=user)
        serializer = self.get_serializer(result, many = True)
        return Response(serializer.data)

