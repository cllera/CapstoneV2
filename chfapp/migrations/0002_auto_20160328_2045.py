# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-28 20:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chfapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nextscene',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='sceneoptions',
            unique_together=set([]),
        ),
    ]