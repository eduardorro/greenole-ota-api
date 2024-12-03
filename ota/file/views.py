from rest_framework.viewsets import ModelViewSet
from .models import File
from .serializer import FileSerializer

class FileViewSet(ModelViewSet):

    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all()
    
    def create(self, request, *args, **kwargs):
        pass
        