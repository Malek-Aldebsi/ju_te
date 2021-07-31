from .models import Assessment, Note
from rest_framework import viewsets, permissions
from .serializers import AssessmentSerializer, NoteSerializer
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .serializers import AssessmentSerializer
from .process.image_processor import buccal
from rest_framework.decorators import action
from fpdf import FPDF
import numpy as np
from django.http import HttpResponse
import cv2
import os


#Assessment viewset
class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class=AssessmentSerializer
    queryset = Assessment.objects.all()

    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        # convert the image to a NumPy array and then read it into
		# OpenCV format
        original = self.request.FILES['original_image']
        name, extention = os.path.splitext(original.name)

        image = np.asarray(bytearray(original.read()), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        #process image using cv2
        notes, image = buccal(image)
        _ , buf = cv2.imencode(extention, image)
            
        #save image in the processed_image field
        content = ContentFile(buf.tobytes())        
        instance = serializer.save()
        instance.processed_image.save(original.name, content)
        
        #create and save instances saved by 
        for note in notes:
            Note.objects.create(note=note, assessment=instance)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            notes = Note.objects.filter(assessment=instance)
            serializer = AssessmentSerializer(instance).data
            serializer['notes'] = NoteSerializer(notes, many=True).data
            return Response(serializer)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=True)
    def report(self, request, *args, **kwargs):
        instance = self.get_object()
        notes = [note.note for note in Note.objects.filter(assessment=instance)]
        name, extention = os.path.splitext(instance.original_image.name)
        
        #
        pdf = FPDF()
        pdf.set_title(name)
        pdf.add_page()
        pdf.image(instance.processed_image.path, w=150, h=250, x=10, y=10)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        for note in notes:
            pdf.cell(60, 10, note, ln=True)
        
        pdf = pdf.output( dest='S').encode('latin-1', errors='ignore')
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' f'"{name}.pdf"'
        response.write(pdf)
        return response
