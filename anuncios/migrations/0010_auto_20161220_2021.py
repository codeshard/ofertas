# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0009_auto_20161220_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='foto',
            field=models.FileField(blank=True, upload_to='productos/fotos/%Y/%m/%d'),
        ),
    ]
