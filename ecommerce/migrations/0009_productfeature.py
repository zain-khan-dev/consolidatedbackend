# Generated by Django 4.0.2 on 2022-05-27 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_rename_image_productimage_src'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='ecommerce.product')),
            ],
        ),
    ]
