# Generated by Django 3.1.3 on 2020-12-18 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0019_auto_20201218_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ManyToManyField(to='restaurants.Food'),
        ),
    ]
