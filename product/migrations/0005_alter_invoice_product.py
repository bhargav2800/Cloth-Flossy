# Generated by Django 4.0.5 on 2022-06-27 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_invoice_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='product.sub_products'),
        ),
    ]