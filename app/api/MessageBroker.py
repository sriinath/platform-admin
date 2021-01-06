from rest_framework.views import APIView, Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from datetime import datetime
from django.db import transaction

from ..models import MessageBroker as MessageBrokerModel
from ..serializers.MessageBroker import MessageBrokerSerializer, SubscriberSerializer
from .helper import get_broker_order
from exception_handler import ExceptionHandler


class MessageBroker(APIView):
    @ExceptionHandler
    def post(self, request):
        with transaction.atomic():
            payload_data = dict()
            if type(request.data) == dict:
                payload_data.update(request.data)

            payload_data.update(created_by=1)

            subscriber_data = payload_data.pop('subscribers', [])
            broker = MessageBrokerSerializer(
                data=payload_data
            )

            if broker.is_valid(raise_exception=True):
                serialized_broker = broker.save()

                for data in subscriber_data:
                    serialized_subscriber_data = dict(
                        data,
                        broker=serialized_broker.id,
                        created_by=1
                    )
                    subscriber = SubscriberSerializer(
                        data=serialized_subscriber_data
                    )

                    if (subscriber.is_valid(raise_exception=True)):
                        subscriber.save()
            
            return Response(
                dict(
                    data=broker.data
                ),
                status=HTTP_201_CREATED
            )


    @ExceptionHandler
    def get(self, request, message_broker_id=None):
        params = request.query_params
        limit = params.get('limit', 24)
        page = params.get('page', 1)
        sort_by = params.get('sort_by', 'asc')
        term = params.get('term')
        filter_query = dict()

        start_index = (page - 1) * limit
        end_index = start_index + limit

        if message_broker_id:
            filter_query.update(
                id=message_broker_id
            )
        else:
            if term:
                filter_query.update(
                    name__contains=term
                )

        return Response(
            MessageBrokerSerializer(
                MessageBrokerModel.objects.filter(
                    **filter_query
                ).order_by(
                    get_broker_order(sort_by)
                )[start_index: end_index],
                many=True
            ).data,
            status=HTTP_200_OK
        )

    @ExceptionHandler
    def put(self, request, message_broker_id):
        with transaction.atomic():
            payload = request.data
            broker = MessageBrokerSerializer(
                MessageBrokerModel.objects.get(id=message_broker_id),
                data=payload,
                partial=True
            )
            if broker.is_valid(raise_exception=True):
                broker.save()
        
        return Response(
            dict(
                data=broker.data
            ),
            status=HTTP_200_OK
        )
