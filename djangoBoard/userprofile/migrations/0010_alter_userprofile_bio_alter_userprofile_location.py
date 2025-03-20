# Generated by Django 5.1.7 on 2025-03-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_alter_userprofile_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default='No bio yet!', max_length=500),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(default='No location yet!', max_length=100),
        ),
    ]
