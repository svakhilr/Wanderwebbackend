# Generated by Django 5.0.7 on 2024-08-20 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0013_alter_tripbooking_booking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripbooking',
            name='booking_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tripbooking',
            name='payment_session_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
