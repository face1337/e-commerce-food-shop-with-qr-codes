# Generated by Django 3.1.3 on 2020-12-18 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0018_auto_20201218_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.ManyToManyField(to='restaurants.Category'),
        ),
    ]
