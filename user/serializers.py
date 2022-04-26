from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "user_role")

    def save(self, **kwargs):
        user = User(
            email=self.validated_data["email"],
            user_role=self.validated_data["user_role"],
        )
        password = self.validated_data["password"]
        if password.isdigit() or password.isalpha():
            raise ValidationError("Password must contains letters and numbers")
        if len(password) <= 8:
            raise ValidationError("Password cannot be less than 8 symbols")
        user.set_password(password)
        user.save()
        return user


class SubscribeCreateSerializer(serializers.Serializer):
    author = serializers.IntegerField()

    def create(self, validated_data):
        obj = Subscription.objects.get_or_create(user=self.context["request"].user)[0]
        author = User.objects.filter(
            id=validated_data["author"], user_role="author"
        ).first()
        obj.author.add(author)
        return obj

    def to_representation(self, instance):
        return {"id": instance.id}
