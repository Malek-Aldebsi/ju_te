# Generated by Django 3.2.5 on 2022-02-06 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_aspect', models.CharField(choices=[('buccal', 'buccal'), ('lingual', 'lingual'), ('mesial', 'mesial'), ('distal', 'distal'), ('top_view', 'top_view')], max_length=20)),
                ('image_type', models.CharField(choices=[('premandibular', 'premandibular'), ('central', 'central')], max_length=20)),
                ('original_image', models.ImageField(upload_to='original')),
                ('processed_image', models.ImageField(blank=True, upload_to='processed')),
                ('shape_match_image', models.ImageField(blank=True, upload_to='shape_match')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=256)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='engine.assessment')),
            ],
        ),
    ]
