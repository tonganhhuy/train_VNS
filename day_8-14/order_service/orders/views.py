from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    # Sử dụng prefetch_related để tối ưu việc load các OrderItem
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
