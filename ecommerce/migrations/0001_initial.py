# Generated by Django 4.0.2 on 2022-04-23 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=2000)),
                ('phone_number', models.CharField(max_length=20)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=2000)),
                ('phone_number', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('stars', models.DecimalField(decimal_places=1, default=5.0, max_digits=2)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='ecommerce.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_ts', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PE', 'Order Pending'), ('PL', 'Order Placed'), ('OFD', 'Out For Delivery'), ('PKD', 'Order Packed'), ('SHP', 'Order Shipping'), ('CMP', 'Order Completed'), ('UNF', 'Unfulfilled')], max_length=40)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ecommerce.customer')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='ecommerce.product')),
            ],
        ),
    ]
