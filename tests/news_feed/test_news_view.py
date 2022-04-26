from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from news_feed.models import Article
from user.models import Subscription, User


class TestCaseWithData(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user_author = User.objects.create_user(
            email="german@mail.ru", password="qwerty123", user_role="author"
        )

        cls.article_open_1 = Article.objects.create(
            type="open", author=cls.user_author, title="rrrrrrrrr", text="sssssssss"
        )
        cls.article_open_2 = Article.objects.create(
            type="open", author=cls.user_author, title="ddasa", text="sssssssdaasss"
        )
        cls.article_open_3 = Article.objects.create(
            type="open", author=cls.user_author, title="vcxvxcvx", text="asdasd"
        )

        cls.article_close_1 = Article.objects.create(
            type="close", author=cls.user_author, title="adssda", text="xzzxxzxzx"
        )

        cls.post_data_article = {
            "type": "close",
            "title": "aspdksa",
            "text": "apsdkasd",
        }

        cls.patch_data = {"title": "print() tema"}

        cls.user_sub = User.objects.create_user(
            email="germanGG@mail.ru", password="qwerty123", user_role="subscriber"
        )

        cls.subscribtion_for_sub = Subscription.objects.create(user=cls.user_sub)
        cls.subscribtion_for_sub.author.add(cls.user_author.id)

        cls.get_open_articles = reverse("article-list")
        cls.create_article_author = reverse("article-news-create")
        cls.get_private_articles = reverse("article-news-private")
        cls.get_article_news_edit = reverse(
            "article-news-edit", args=[f"{cls.article_open_3.id}"]
        )


class TestWithAnonymousOpenNewsList(TestCaseWithData):
    def test_response_status_code(self):
        response = self.client.get(self.get_open_articles)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_quantity_news(self):
        response = self.client.get(self.get_open_articles)
        self.assertEqual(len(response.data), 3)


class TestWithAnonymousCreate(TestCaseWithData):
    def test_response_status_code(self):
        response = self.client.post(self.create_article_author, self.post_data_article)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestWithSubCreate(TestCaseWithData):
    def setUp(self) -> None:
        token = RefreshToken.for_user(self.user_sub)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_response_status_code(self):
        response = self.client.post(self.create_article_author, self.post_data_article)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestWithAuthorCreate(TestCaseWithData):
    def setUp(self) -> None:
        token = RefreshToken.for_user(self.user_author)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_response_status_code(self):
        response = self.client.post(self.create_article_author, self.post_data_article)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_object_exists(self):
        self.client.post(self.create_article_author, self.post_data_article)
        obj = Article.objects.filter(
            type=self.post_data_article["type"],
            text=self.post_data_article["text"],
            title=self.post_data_article["title"],
        ).first()
        self.assertTrue(obj)


class TestWithAnonymousPrivate(TestCaseWithData):
    def test_status_code(self):
        response = self.client.get(self.get_private_articles)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestWithAuthorizedPrivate(TestCaseWithData):
    def setUp(self) -> None:
        token = RefreshToken.for_user(self.user_sub)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_status_code(self):
        response = self.client.get(self.get_private_articles)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_no_empty(self):
        response = self.client.get(self.get_private_articles)
        self.assertTrue(response.data)
        self.assertEqual(response.data[0]["author"], self.user_author.email)


class TestWithAuthorEdit(TestCaseWithData):
    def setUp(self) -> None:
        token = RefreshToken.for_user(self.user_author)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.access_token}")

    def test_status_code(self):
        response = self.client.patch(self.get_article_news_edit, self.patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_data(self):
        response = self.client.patch(self.get_article_news_edit, self.patch_data)
        self.assertEqual(response.data["title"], self.patch_data["title"])
