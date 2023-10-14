from django.shortcuts import render
from django.db.models import Subquery, OuterRef, Q

from rest_framework import generics

from api.serializers import MessageSerializer
from api.models import ChatMessage, User
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