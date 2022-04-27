from news_feed.models import Article
from user.models import Subscription


def private_news_list(user):
    if Subscription.objects.all().exists() and Article.objects.all().exists():
        authors = list(
            Subscription.objects.prefetch_related("author")
            .filter(user=user)
            .first()
            .author.all()
        )
        return Article.objects.filter(author__in=authors, type="close").select_related(
            "author"
        )


def author_article_list(user):
    return Article.objects.filter(author=user)
