# Generated by Django 3.0 on 2021-09-06 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20210906_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
