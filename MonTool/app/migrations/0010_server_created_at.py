# Generated by Django 4.2.20 on 2025-05-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_server_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
