# Generated by Django 5.0.1 on 2024-02-29 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_robot_f1_robot_f2'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='brok',
            field=models.TextField(blank=True, null=True),
        ),
    ]
