# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('topic_name', models.CharField(max_length=30)),
                ('topic_id', models.IntegerField(max_length=10)),
                ('domain_id', models.IntegerField(max_length=5)),
            ],
        ),
    ]
