# Generated by Django 5.0.1 on 2024-01-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_device_urln'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='firs',
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
    ]
