# Generated by Django 5.0.7 on 2024-07-20 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_rename_dicription_packageitnary_discription'),
    ]

    operations = [
        migrations.AddField(
            model_name='trippackage',
            name='location',
            field=models.CharField(max_length=70, null=True),
        ),
    ]
