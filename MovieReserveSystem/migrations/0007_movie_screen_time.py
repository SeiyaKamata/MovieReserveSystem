# Generated by Django 4.2.2 on 2023-07-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieReserveSystem', '0006_schedule_hole'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='screen_time',
            field=models.IntegerField(default=90, help_text='上映時間'),
        ),
    ]