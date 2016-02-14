# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-13 23:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chfapp', '0005_auto_20160213_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=100)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chfapp.Users')),
            ],
        ),
    ]
