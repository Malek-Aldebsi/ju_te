from django.db import models

class Assessment(models.Model):
    IMAGE_ASPECT = [
        ("buccal", "buccal"),
        ("lingual", "lingual"),
        ("mesial", "mesial"),
        ("distal", "distal"),
        ("top_view", "top_view")
    ]

    image_aspect = models.CharField(
        max_length=20,
        choices=IMAGE_ASPECT
    )

    IMAGE_TYPE= [
        ("mandipular", "mandipular"),
        ("central", "central"),
    ]

    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE,
    )

    original_image = models.ImageField(upload_to="original")
    processed_image = models.ImageField(upload_to="processed", blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


class Note(models.Model):
    assessment = models.ForeignKey(Assessment, related_name='notes', on_delete=models.CASCADE)
    note = models.CharField(max_length=256, blank=False)
    
    def __str__(self) -> str:
        return self.note