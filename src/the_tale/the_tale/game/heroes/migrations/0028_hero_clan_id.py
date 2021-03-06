# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-11-05 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clans', '0008_clan_state'),
        ('heroes', '0027_reset_heroes_actions'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='clan_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='clans.Clan'),
        ),
    ]
