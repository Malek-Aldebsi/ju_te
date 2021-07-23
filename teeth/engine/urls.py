from django.urls import path
from .views import upload
from rest_framework.routers import DefaultRouter
from .api import AssessmentViewSet

router = DefaultRouter()
router.register(r'api/assessments', AssessmentViewSet, basename='assessment')


urlpatterns=[
    path('upload/', upload),
    *router.urls
]