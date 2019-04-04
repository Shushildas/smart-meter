# Generated by Django 2.2 on 2019-04-02 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MeterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=13)),
                ('meter_id', models.CharField(max_length=50)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rest.Profile')),
            ],
            options={
                'unique_together': {('meter_id', 'profile', 'contact_number')},
            },
        ),
        migrations.CreateModel(
            name='MeterManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(max_length=13)),
                ('group_num', models.IntegerField()),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rest.Profile')),
            ],
            options={
                'unique_together': {('group_num', 'profile', 'contact_number')},
            },
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('volt', models.FloatField()),
                ('current', models.FloatField()),
                ('watt', models.FloatField()),
                ('power', models.FloatField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.MeterUser')),
            ],
            options={
                'unique_together': {('profile', 'timestamp')},
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.MeterManager')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rest.MeterUser')),
            ],
            options={
                'unique_together': {('user', 'manager')},
            },
        ),
    ]