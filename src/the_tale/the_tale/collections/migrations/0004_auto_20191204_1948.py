# Generated by Django 2.1.15 on 2019-12-04 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collections', '0003_auto_20161019_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='approved',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='approved',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='kit',
            name='approved',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]