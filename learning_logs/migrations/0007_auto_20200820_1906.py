# Generated by Django 3.1 on 2020-08-20 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0006_auto_20200820_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='image',
            field=models.ImageField(default='default.png', upload_to='images_entries/', verbose_name='Image'),
        ),
    ]
