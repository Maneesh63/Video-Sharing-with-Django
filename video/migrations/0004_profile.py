# Generated by Django 5.0.7 on 2024-07-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_videostore_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=2000, null=True)),
                ('ppic', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
            ],
        ),
    ]
