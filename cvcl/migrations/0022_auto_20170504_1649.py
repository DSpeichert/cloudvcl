# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-04 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvcl', '0021_auto_20170504_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vmdefinition',
            name='package_reboot_if_required',
            field=models.NullBooleanField(help_text='(Linux-only)', verbose_name='Perform reboot if required after package install/upgrade'),
        ),
        migrations.AlterField(
            model_name='vmdefinition',
            name='package_update',
            field=models.NullBooleanField(help_text='(Linux-only)', verbose_name='Update package lists on boot'),
        ),
        migrations.AlterField(
            model_name='vmdefinition',
            name='package_upgrade',
            field=models.NullBooleanField(help_text='(Linux-only)', verbose_name='Upgrade all packages on boot'),
        ),
    ]
