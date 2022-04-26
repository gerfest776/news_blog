from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import Subscription, User


class TestCaseWithData(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post_data = {
            "email": "german2222@mail.ru",
            "password": "qwerty123",
            "user_role": "author",
        }
        cls.incorrect_data_password = {
            "email": "german@mail.ru",
            "password": "qwertyhji",
            "user_role": "author",
        }
        cls.incorrect_data_email = {
            "email": "german",
            "password": "qwertyhji123",
            "user_role": "author",
        }

        cls.user_author = User.objects.create_user(
            email="german@mail.ru", password="qwerty123", user_role="author"
        )
        cls.user_sub = User.objects.create_user(
            email="germanGG@mail.ru", password="qwerty123", user_role="subscriber"
        )

        cls.post_data_sub_view = {"author": cls.user_author.id}

        cls.url_create_user = reverse("user-list")
        cls.url_create_subscription = reverse("user-subscribe")


class TestCreateUser(TestCaseWithData):
    def test_response_code(self):
        response = self.client.post(self.url_create_user, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_created_data(self):
        self.client.post(self.url_create_user, self.post_data)
        self.assertTrue(User.objects.all().exists())

    def test_incorrect_password(self):
        response = self.client.post(self.url_create_user, self.incorrect_data_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_email(self):
        response = self.client.post(self.url_create_user, self.incorrect_data_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestSubscribeUserAnonymous(TestCaseWithData):
    def test_no_auth(self):
        response = self.client.post(
            self.url_create_subscription, self.post_data_sub_view
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestSubscribeUserAuthorized(TestCaseWithData):
    def setUp(self) -> None:
        token = RefreshToken.for_user(self.user_sub)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_status_code(self):
        response = self.client.post(
            self.url_create_subscription, self.post_data_sub_view
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_data(self):
        self.client.post(self.url_create_subscription, self.post_data_sub_view)
        self.assertTrue(Subscription.objects.all().exists())

        relations = list(Subscription.objects.all().first().author.all())
        self.assertTrue(self.user_author in relations)
