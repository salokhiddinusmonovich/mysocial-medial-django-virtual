# Generated by Django 5.0.6 on 2024-06-17 11:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0003_remove_supportme_paid_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportme',
            name='author',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_me', to=settings.AUTH_USER_MODEL),
        ),
    ]
