from rest_framework import viewsets

from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    # Sử dụng prefetch_related để tối ưu hóa việc lấy CartItem (N+1 query problem)
    queryset = Cart.objects.prefetch_related("items").all()
    serializer_class = CartSerializer

    def get_queryset(self):
        # Trả về giỏ hàng của user hiện tại
        return self.queryset
