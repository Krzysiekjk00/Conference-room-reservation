# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-20 13:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together=set([('room', 'date')]),
        ),
    ]
