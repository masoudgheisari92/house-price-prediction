# Generated by Django 4.1.6 on 2023-03-10 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_house_num_room_house_link_house_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='floor',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='house',
            name='link',
            field=models.URLField(max_length=256),
        ),
    ]