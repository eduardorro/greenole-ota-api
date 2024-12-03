from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from .models import File
from typing import Any
from .service import FileService

class FileAdmin(admin.ModelAdmin):
    def save_model(self, request: HttpRequest, obj: Any, form: ModelForm, change: bool) -> None:
        service = FileService(file=obj, **request.FILES)
        service.save()


admin.site.register(File, FileAdmin)