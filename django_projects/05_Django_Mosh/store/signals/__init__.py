"""
here is where we difine our signals:



"""

from django.dispatch import Signal

# create signal object
order_created_signal = Signal()

# wee need to fire this signal when an Order is created: inside of CreateOrderModelSerializer

