# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sml_auction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='current_bet',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='active_item', to='sml_auction.Bet', verbose_name='Bet'),
        ),
    ]
