import uuid
import random

from datetime import timedelta
from django.utils import timezone


def create_uuid():
    return str(uuid.uuid1().int >> 64)


def create_random_name():
    name = f"zzz{str(uuid.uuid1().int >> 64)[:6]}"
    return name


def create_code():
    return random.randint(124578, 987593)


def code_expiration():
    return timezone.now() + timedelta(minutes=5)
