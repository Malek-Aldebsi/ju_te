from django.db import models

class Process(models.Model):
    original_image = models.ImageField(upload_to="original")
    processed_image = models.ImageField(upload_to="processed")
