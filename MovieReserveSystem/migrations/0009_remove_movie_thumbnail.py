# Generated by Django 4.2.2 on 2023-07-27 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MovieReserveSystem', '0008_movie_poster'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='thumbnail',
        ),
    ]