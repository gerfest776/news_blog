from django.db import IntegrityError
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
        try:
            return Article.objects.create(
                **validated_data, author=self.context["request"].user
            )
        except IntegrityError as e:
            raise Exception("That article already exists") from e


class NewsEditSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("type", "title", "text")
        extra_kwargs = {
            "type": {"required": False},
            "title": {"required": False},
            "text": {"required": False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
