from django.urls import path
from api.views import MyInbox, GetMessages, ProfileDetail, SendMessage, Search

urlpatterns = [
    path('my-messages/<user_id>', MyInbox.as_view(), name="inbox"),
    path('profile/<int:pk>', ProfileDetail.as_view(), name="profile"),
    path('send-message', SendMessage.as_view(), name="send-message"),
    path('get-message/<sender_id>/receiver_id', GetMessages.as_view(), name = "messages-between-2-people"),
    path('search/<search>', Search.as_view(), name = "search"),
]