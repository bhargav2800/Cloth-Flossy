# Generated by Django 4.0.5 on 2022-07-13 05:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_alter_sub_products_color_alter_sub_products_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='returned_last_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
