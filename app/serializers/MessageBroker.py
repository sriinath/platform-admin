from rest_framework import serializers
from datetime import datetime

from ..models import MessageBroker, Subscriber


class MessageBrokerSerializer(serializers.ModelSerializer):
    broker_status = serializers.SerializerMethodField()
    created_by_user = serializers.SerializerMethodField()

    class Meta:
        model = MessageBroker
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'write_only': True},
            'status': {'write_only': True}
        }
    
    def get_created_by_user(self, obj):
        return obj.created_by.username

    def get_broker_status(self, obj):
        return obj.get_status_display()
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
