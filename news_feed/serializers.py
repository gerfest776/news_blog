from rest_framework import serializers

from news_feed.models import Article


class NewsListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ("author", "title", "text", "time_create")


class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "type",
            "title",
            "text",
        )

    def create(self, validated_data):
        if Article.objects.filter(
                **validated_data, author=self.context["request"].user
        ).exists():
            raise Exception("That article already exists")

        return Article.objects.create(
            **validated_data, author=self.context["request"].user
        )



class NewsEditSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("type", "title", "text")
        extra_kwargs = {
            "type": {"required": False},
            "title": {"required": False},
            "text": {"required": False},
        }
