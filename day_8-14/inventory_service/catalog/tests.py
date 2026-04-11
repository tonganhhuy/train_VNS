from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product, Stock


class InventoryTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Gadgets")
        self.product = Product.objects.create(
            category=self.category,
            name="Smartphone",
            description="A high-end smartphone",
            price=999.99,
        )
        self.stock = Stock.objects.create(product=self.product, quantity=10)

        self.user = User.objects.create_user(username="staff", password="password123")
        self.list_url = "/api/products/"

    def test_product_list_public(self):
        # Public access
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["name"], "Smartphone")

    def test_create_product_unauthenticated(self):
        # Unauthenticated creation should fail
        data = {"category": self.category.id, "name": "Laptop", "price": 1500.00}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_authenticated(self):
        # Authenticated creation should succeed
        self.client.force_authenticate(user=self.user)
        data = {"category": self.category.id, "name": "Laptop", "price": 1500.00}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Laptop")
