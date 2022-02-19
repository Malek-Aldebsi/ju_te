from datetime import datetime
from .google_service import Create_Service
from .models import Assessment, Note
from rest_framework import viewsets, permissions
from .serializers import AssessmentSerializer, NoteSerializer
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from .serializers import AssessmentSerializer
from .process.buccal import buccal
from .process.distal import distal
from .process.mesial import mesial
from .process.lingual import lingual
from .process.top_view import top_view
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from fpdf import FPDF
import numpy as np
from django.http import HttpResponse
import cv2
import os
from django.conf import settings
from googleapiclient.http import MediaIoBaseUpload
import io
import traceback
from PIL import Image
from PIL.ExifTags import TAGS

processors = {
    "buccal": buccal,
    "distal": distal,
    "mesial": mesial,
    "lingual": lingual,
    "top_view": top_view
}

#Assessment viewset
class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class=AssessmentSerializer
    queryset = Assessment.objects.all()

    permission_classes = [permissions.AllowAny]
    

    def save_to_drive(self, media=None, metadata=None):
        creds = os.path.join(settings.BASE_DIR, "credentials.json") 
        API_NAME="drive"
        API_VERSION="v3"
        SCOPES=["https://www.googleapis.com/auth/drive"]
        service = Create_Service(creds, API_NAME, API_VERSION, SCOPES)
        service.files().create(
            body=metadata,
            media_body=media,
            fields='id'
        ).execute()

    def perform_create(self, serializer):
      
        # convert the image to a NumPy array and then read it into
		# OpenCV format
        original = self.request.FILES['original_image']
        _, extention = os.path.splitext(original.name)

        image = np.asarray(bytearray(original.read()), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

        #process image using cv2
        image_aspect = self.request.data['image_aspect']
        image_type = self.request.data['image_type']

        try:
            notes, processed_image, shape_image = processors[image_aspect](image, image_type)
            _ , processed_buf = cv2.imencode(extention, processed_image)
            _, shape_buf = cv2.imencode(extention, shape_image)
        except Exception as exp:
            #saving the stacktrace
            self.save_to_drive(
                metadata={
                    'name': datetime.now().strftime("%Y-%m-%d_%H:%M__") + original.name + "__stacktrace.txt",
                    'parents': ['1Il0N-_bNoKIIpvdDPfGVq4A_BnNUIFk3'], 
                    'mimeType': 'text/plain'},
                media=MediaIoBaseUpload(io.BytesIO(f"{str(exp)}\n{traceback.format_exc()}".encode('utf-8')), mimetype='text/plain')
            )
            #saving the faulty image
            self.save_to_drive(
                metadata={
                    'name': datetime.now().strftime("%Y-%m-%d_%H:%M__") + original.name , 
                    'parents': ['1lUOmX7_MWmfyCGIMccpFbMkrkmDWKZqu'], 
                    'mimeType': 'image/jpeg'},
                media=MediaIoBaseUpload(io.BytesIO(cv2.imencode('.jpg', image)[1].tobytes()), mimetype='image/jpeg')
            )

            #saveing the image properties 
            img = Image.open(original)
            exifdata = img.getexif()
            tags = []
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                # decode bytes 
                if isinstance(data, bytes):
                    data = data.decode()
                tags.append(f"{tag:25}: {data}\n")
            tags = "".join(tags)
            print("tags",str(exifdata))
            self.save_to_drive(
                metadata={
                    'name': datetime.now().strftime("%Y-%m-%d_%H:%M__") + original.name + "__metadata.txt",
                    'parents': ['1di4VuKdNCVeQjGChme9VUBxPdEt2H9BG'], 
                    'mimeType': 'text/plain'},
                media=MediaIoBaseUpload(io.BytesIO(tags.encode('utf-8')), mimetype='text/plain')
            )

            raise APIException(exp)
        #save image in the processed_image field
        processed_content = ContentFile(processed_buf.tobytes())   
        shape_content = ContentFile(shape_buf.tobytes())     
        instance = serializer.save()
        instance.processed_image.save(original.name, processed_content)
        instance.shape_match_image.save(original.name, shape_content)
        
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
        
        pdf = FPDF()
        pdf.set_title(name)
        pdf.add_page()
        pdf.image(instance.processed_image.path, w=120, x=40, y=5)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_y(180)
        for note in notes:
            pdf.cell(60, 8, "-" + note, ln=True)
        
        pdf = pdf.output( dest='S').encode('latin-1', errors='ignore')
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' f'"{name}.pdf"'
        response.write(pdf)
        return response
