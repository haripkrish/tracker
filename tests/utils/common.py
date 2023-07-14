import uuid
import random
import string


def get_random_uuid() -> uuid:
    return uuid.uuid4()


def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def get_random_int():
    return random.randint(0, 10000)


def get_random_city():
    city = ['Berlin', 'Paris', 'Rome', 'Bangalore']
    return random.choice(city)


def get_random_price():
    random.random()
