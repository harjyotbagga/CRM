# Generated by Django 3.0.5 on 2020-04-12 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200413_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_name='product_tags', to='accounts.Tag'),
        ),
    ]