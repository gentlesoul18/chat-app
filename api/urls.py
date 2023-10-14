from django.urls import path
from api.views import MyInbox

urlpatterns = [
    path('messages/<user_id>', MyInbox.as_view(), name="messages"),
]