# Generated by Django 3.2.5 on 2021-07-26 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0007_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessment',
            name='note',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='permanent',
        ),
        migrations.AlterField(
            model_name='assessment',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
