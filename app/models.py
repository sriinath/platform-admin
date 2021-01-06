from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MessageBroker(models.Model):
    name = models.TextField(
        unique=True,
        db_index=True
    )
    description = models.TextField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    status = models.IntegerField(
        null=False, blank=False,
        choices=(
            (1, 'Created'),
            (2, 'Available')
        ),
        default=1
    )


class Subscriber(models.Model):
    url = models.URLField()
    headers = models.TextField()
    broker = models.ForeignKey(MessageBroker, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

