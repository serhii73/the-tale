# Generated by Django 2.1.15 on 2019-12-04 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0009_auto_20191204_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='is_declined',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
