from .models import Assessment, Note
from rest_framework import viewsets, permissions
from .serializers import AssessmentSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .serializers import AssessmentSerializer
from .process.image_processor import buccal
import numpy as np
import cv2
import os


#Assessment viewset
class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class=AssessmentSerializer
    queryset = Assessment.objects.all()

    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
       
        """
        file = self.request.FILES['original_image']
        image = Image.open(file)
        format = image.format
        image = image.rotate(90.0)
        image_bytes = BytesIO()
        image.save(image_bytes, format=format)
        image = InMemoryUploadedFile(
            file=image_bytes,
            field_name=None,
            name=file.name,
            content_type=file.content_type,
            size=file.size,
            charset=None
        )
        """

        # convert the image to a NumPy array and then read it into
		# OpenCV format
        original = self.request.FILES['original_image']
        name, extention = os.path.splitext(original.name)

        image = np.asarray(bytearray(original.read()), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        #process image using cv2
        notes, image = buccal(image)
        _ , buf = cv2.imencode(extention, image)
    
        print(f"notes: {notes}")
            
        #save image in the processed_image field
        content = ContentFile(buf.tobytes())        
        instance = serializer.save()
        instance.processed_image.save(original.name, content)
        
        #create and save instances saved by 
        for note in notes:
            Note.objects.create(note=note, assessment=instance)
    """
    @action(detail=True)
    def process(self, request, *args, **kwargs):
        assessment = Assessment.objects.get(pk=request.data['id'])

        
        image = Image.open(assessment.processed_image)
        format = image.format
        image = image.rotate(90.0)
        image_bytes =BytesIO()
        image.save(image_bytes, format=format)
        image = InMemoryUploadedFile(
            file=image_bytes,
            field_name=None,
            name=assessment.processed_image.name,
            content_type='image/jpeg',
            size=image.tell,
            charset=None
        )
        assessment.processed_image.save(assessment.processed_image.name, image)
        assessment.save()
        return Response(AssessmentSerializer(assessment).data)
        """

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)