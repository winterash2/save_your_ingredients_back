# Generated by Django 3.1.3 on 2020-11-11 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='amount',
            field=models.IntegerField(),
        ),
    ]