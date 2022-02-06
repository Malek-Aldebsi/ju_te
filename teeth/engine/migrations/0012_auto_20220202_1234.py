# Generated by Django 3.2.5 on 2022-02-02 12:34

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0011_errorlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='image',
            field=models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='errlog_images'),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='stacktrace',
            field=models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='errlog_stacktrace'),
        ),
    ]