# Generated by Django 5.0.7 on 2024-08-09 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='assets/profileavatar.png', null=True, upload_to='customer/profile'),
        ),
    ]
