# Generated by Django 3.1.4 on 2021-05-10 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourdiary', '0006_auto_20210510_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='color',
            field=models.CharField(default='#000000', max_length=20),
        ),
        migrations.AddField(
            model_name='tasks',
            name='icon',
            field=models.CharField(default='fa-question', max_length=20),
        ),
    ]
