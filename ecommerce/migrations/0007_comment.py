# Generated by Django 4.0.2 on 2022-05-25 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_productspecification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=2000)),
                ('comment_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ecommerce.profileuser')),
                ('comment_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ecommerce.product')),
            ],
        ),
    ]
