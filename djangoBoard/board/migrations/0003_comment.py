# Generated by Django 5.1.7 on 2025-03-15 22:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_remove_ad_category_ad_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ad', models.ManyToManyField(related_name='comments', to='board.ad')),
                ('user', models.ManyToManyField(related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
