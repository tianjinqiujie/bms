# Generated by Django 2.0.4 on 2018-07-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20180705_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='now_time',
            field=models.DateTimeField(null=True),
        ),
    ]
