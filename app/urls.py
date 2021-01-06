from django.urls import path
from .api.MessageBroker import MessageBroker

urlpatterns = [
    path('broker/message/', MessageBroker.as_view()),
    path('broker/message/<int:message_broker_id>', MessageBroker.as_view()),
]
