# Generated by Django 3.1.3 on 2020-11-29 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201129_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='flat_number',
            field=models.CharField(blank=True, max_length=60, verbose_name='Nr mieszkania:'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='house_number',
            field=models.CharField(default='0', max_length=60, verbose_name='Nr bloku/domu:'),
        ),
    ]
