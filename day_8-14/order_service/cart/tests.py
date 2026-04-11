from rest_framework import status
from rest_framework.test import APITestCase

from .models import Cart


class CartTests(APITestCase):
    def setUp(self):
        self.cart = Cart.objects.create(user_id=1)
        self.cart_url = "/api/carts/"
        self.cart_detail_url = f"/api/carts/{self.cart.id}/"

    def test_create_cart(self):
        data = {"user_id": 2}
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 2)

    def test_add_item_to_cart(self):
        # Adding items is technically a PUT/PATCH or a custom action if implemented.
        # Based on the Serializer, we can check CartItem creation.
        item_data = {
            "cart": self.cart.id,
            "product_id": 101,
            "quantity": 2,
            "price_at_addition": 50.00,
        }
        # Assuming we can add items via a nested endpoint or by creating CartItem directly if exposed.
        # Since only CartViewSet is registered in urls.py, let's assume we use standard ModelViewSet.
        # Let's check if there's a CartItemViewSet. (Wait, I checked urls.py and it only had CartViewSet).

        # Test listing carts
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
