# Generated by Django 4.2.1 on 2023-05-11 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delevery', 'Out for delevery'), ('Deliverd', 'Delivered')], max_length=50, null=True),
        ),
    ]
