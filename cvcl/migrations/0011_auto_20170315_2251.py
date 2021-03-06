# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvcl', '0010_auto_20170315_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='min_disk',
            field=models.IntegerField(default=0, verbose_name='Min ram in GB'),
        ),
        migrations.AlterField(
            model_name='image',
            name='min_ram',
            field=models.IntegerField(default=0, verbose_name='Min ram in MB'),
        ),
        migrations.AlterField(
            model_name='user',
            name='limit_ram',
            field=models.IntegerField(default=0, verbose_name='RAM limit in MB'),
        ),
        migrations.AlterField(
            model_name='user',
            name='usage_ram',
            field=models.IntegerField(default=0, verbose_name='RAM usage in MB'),
        ),
    ]
