# Generated by Django 3.2.5 on 2021-07-19 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='original')),
                ('processed_image', models.ImageField(upload_to='processed')),
                ('note', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='Process',
        ),
    ]