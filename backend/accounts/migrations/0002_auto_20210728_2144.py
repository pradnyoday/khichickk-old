# Generated by Django 2.2 on 2021-07-28 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='users',
            name='last_name',
            field=models.CharField(default='None', max_length=200),
            preserve_default=False,
        ),
    ]
