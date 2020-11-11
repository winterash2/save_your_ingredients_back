# Generated by Django 3.1.3 on 2020-11-11 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('trim', models.TextField(default='')),
                ('keep', models.TextField(default='')),
                ('buy', models.TextField(default='')),
            ],
        ),
    ]
