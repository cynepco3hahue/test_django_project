# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('log_collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_name',
            field=models.CharField(validators=[django.core.validators.MinLengthValidator(1)], max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='host_root_password',
            field=models.CharField(validators=[django.core.validators.MinLengthValidator(1)], max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='host_root_user',
            field=models.CharField(validators=[django.core.validators.MinLengthValidator(1)], max_length=20),
            preserve_default=True,
        ),
    ]
