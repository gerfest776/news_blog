# Generated by Django 4.0.4 on 2022-04-26 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news_feed", "0002_article_type"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Rating",
        ),
    ]
