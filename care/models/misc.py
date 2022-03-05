import random
import string
import time

from django.db import models

from arike.users.models import User


def generate_token():
    random.seed(time.time())
    random.choice(string.ascii_letters + string.digits)
    return "".join([random.choice(string.ascii_letters+string.digits) for _ in range(30)])


class TemporaryLink(models.Model):
    token = models.CharField(default=generate_token, null=False, blank=False, max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
