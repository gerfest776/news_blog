# Generated by Django 4.0.4 on 2022-04-26 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news_feed", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="type",
            field=models.CharField(
                choices=[("open", "Open"), ("close", "Closed")],
                max_length=10,
                null=True,
            ),
        ),
    ]
