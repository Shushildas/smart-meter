# Generated by Django 2.2 on 2019-04-02 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.MeterUser'),
        ),
    ]