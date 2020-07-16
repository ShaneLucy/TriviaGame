# Generated by Django 3.0.8 on 2020-07-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0003_auto_20200716_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice',
            name='time_taken',
        ),
        migrations.AddField(
            model_name='practice',
            name='time_taken_seeconds',
            field=models.CharField(default=55, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='practice',
            name='score',
            field=models.CharField(max_length=3),
        ),
    ]
