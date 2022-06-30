# Generated by Django 4.0.5 on 2022-06-29 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_order_order_status_alter_order_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
        migrations.AddField(
            model_name='invoice',
            name='order_status',
            field=models.CharField(choices=[('Not Packed', 'Not Packed'), ('Ready For Shipment', 'Ready For Shipment'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Not Packed', max_length=20),
        ),
    ]
