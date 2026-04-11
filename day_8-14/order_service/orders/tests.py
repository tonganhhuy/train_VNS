from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order, OrderItem


class OrderTests(APITestCase):
    def setUp(self):
        self.order_url = "/api/orders/"
        self.order = Order.objects.create(user_id=1, total_price=150.00)
        self.item = OrderItem.objects.create(
            order=self.order, product_id=101, quantity=1, price=150.00
        )

    def test_list_orders(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(float(response.data[0]["total_price"]), 150.00)

    def test_create_order(self):
        data = {"user_id": 2, "status": "pending", "total_price": 200.00}
        response = self.client.post(self.order_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
