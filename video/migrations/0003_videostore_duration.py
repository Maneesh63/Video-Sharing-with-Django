# Generated by Django 5.0.7 on 2024-07-21 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_videostore_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='videostore',
            name='duration',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
