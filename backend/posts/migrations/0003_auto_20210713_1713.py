# Generated by Django 2.2 on 2021-07-13 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210713_1510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shares',
            options={'verbose_name_plural': 'Shares'},
        ),
        migrations.AlterField(
            model_name='posts',
            name='caption',
            field=models.TextField(max_length=10000),
        ),
    ]