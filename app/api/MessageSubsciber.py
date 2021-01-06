from rest_framework.views import APIView, Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from datetime import datetime
from django.db import transaction

from ..models import Subscriber as Subscriber
from ..serializers.MessageBroker import SubscriberSerializer
from .helper import get_broker_order
from exception_handler import ExceptionHandler


class MessageSubsciber(APIView):
    @ExceptionHandler
    def post(self, request, message_broker_id):
        with transaction.atomic():
            payload_data = dict(
                created_by=1
            )

            if type(request.data) == dict:
                payload_data.update(request.data)

            subscriber = SubscriberSerializer(
                data=payload_data
            )

            if subscriber.is_valid(raise_exception=True):
                subscriber.save()
        
        return Response(
            dict(
                status= 'Success',
                data=subscriber.data
            ),
            status=HTTP_201_CREATED
        )


    @ExceptionHandler
    def get(self, request, message_broker_id):
        params = request.query_params
        limit = params.get('limit', 24)
        page = params.get('page', 1)
        start_index = (page - 1) * limit
        end_index = start_index + limit

        return Response(
            MessageBrokerSerializer(
                MessageBrokerModel.objects.filter(
                    id=message_broker_id
                )[start_index: end_index],
                many=True
            ).data,
            status=HTTP_200_OK
        )
