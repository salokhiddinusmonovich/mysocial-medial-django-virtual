# Generated by Django 5.0.6 on 2024-06-17 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0002_supportme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportme',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='supportme',
            name='razorpay_payment_id',
        ),
    ]