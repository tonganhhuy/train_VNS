from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/auth/users/"
        self.login_url = "/api/auth/jwt/create/"
        self.me_url = "/api/auth/users/me/"
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        }

    @patch("django.core.mail.send_mail")
    def test_registration_success(self, mock_send_mail):
        """Test successful registration with mocked email."""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.user_data["username"])

    def test_registration_missing_data(self):
        """Test registration with missing fields."""
        data = {"username": "onlyuser"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate(self):
        """Test duplicate registration error."""
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_password(self):
        """Test login with wrong password."""
        self.client.post(self.register_url, self.user_data)
        login_data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        """Test login with user that doesn't exist."""
        login_data = {"username": "nobody", "password": "nopassword"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_unauthenticated(self):
        """Test accessing profile without token."""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_auth_flow(self):
        """Test registration, login and profile access."""
        # 1. Register
        self.client.post(self.register_url, self.user_data)

        # 2. Login
        login_data = {"username": "testuser", "password": "testpassword123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]

        # 3. Access Me
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
