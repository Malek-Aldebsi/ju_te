import io
from django.http.response import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from .models import Process

@csrf_exempt
def upload(request):
    if request.method == "POST":
        file = request.FILES['file']
        image = Image.open(file)
        format_ = image.format
        image = image.rotate(45.0)
        image_bytes = BytesIO()
        image.save(image_bytes, format=format_)

        image = InMemoryUploadedFile(
            file=image_bytes,
            field_name=None,
            name=file.name,
            content_type=file.content_type,
            size=file.size,
            charset=None
        )

        process = Process.objects.create(original_image=file, processed_image=image)
        process.save()
    
        return JsonResponse({"processed_file_path": process.processed_image.url})
    else:
        return None

