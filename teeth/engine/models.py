from django.db import models

class Assessment(models.Model):


    IMAGE_ASPECT = [
        ("Labial", "Labial"),
        ("Lingual", "Lingual"),
        ("Mesial", "Mesial"),
        ("Destial", "Destial"),
        ("top view", "top view")
    ]

    image_aspect = models.CharField(
        max_length=20,
        choices=IMAGE_ASPECT
    )

    IMAGE_TYPE= [
        ("type 1", "type 1"),
        ("Others", "Others"),
    ]

    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE,
    )

    original_image = models.ImageField(upload_to="original")
    processed_image = models.ImageField(upload_to="processed", blank=True)
    note = models.CharField(max_length=256, blank=True)
    permanent= models.BooleanField(default=False)
    submitted_at = models.DateField(auto_now_add=True)
    