# Generated by Django 5.0.7 on 2024-07-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ppic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
