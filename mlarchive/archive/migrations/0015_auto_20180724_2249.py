# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-24 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    """Decrease size of indexed fields.  When switching from utf8mb3 to utf8mb4, storage
    requirements increase from 3 bytes to 4 bytes per character.  MyISAM tables have a
    maximum index size of 1000, or VARCHAR(250)
    """

    dependencies = [
        ('archive', '0014_auto_20180613_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='filename',
            field=models.CharField(max_length=65),
        ),
        migrations.AlterField(
            model_name='emaillist',
            name='alias',
            field=models.CharField(blank=True, max_length=65),
        ),
        migrations.AlterField(
            model_name='emaillist',
            name='name',
            field=models.CharField(db_index=True, max_length=65, unique=True),
        ),
        migrations.AlterField(
            model_name='legacy',
            name='msgid',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='message',
            name='msgid',
            field=models.CharField(db_index=True, max_length=240),
        ),
    ]
