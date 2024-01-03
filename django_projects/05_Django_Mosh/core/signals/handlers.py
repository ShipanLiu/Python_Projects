"""
here is handlers for handling the signals



"""

from store.signals import order_created_signal
from store.serializers import OrderModalSerializer

from django.dispatch import receiver

@receiver(order_created_signal)
def order_created_handler(sender, **kwargs):
    print("a new order is created")
    print(kwargs["order"])
    print(kwargs["order"].id)

    order = kwargs.get("order")
    # create sLizer
    sLizer = OrderModalSerializer(order)
    # print data
    print(sLizer.data)

