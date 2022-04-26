from django.db import models

from user.models import User


class Article(models.Model):
    class ArticleType(models.TextChoices):
        OPEN = "open"
        CLOSED = "close"

    type = models.CharField(max_length=10, choices=ArticleType.choices, null=True)
    author = models.ForeignKey(User, related_name="article", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["author", "title", "text"]
        db_table = "article"
