# Generated by Django 2.2 on 2019-04-05 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0004_auto_20190405_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='time',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='record',
            name='time',
            field=models.CharField(max_length=50),
        ),
    ]