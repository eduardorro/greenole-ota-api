from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from .models import Version
from typing import Any
from .service import VersionService


@admin.action(description="Mark as latest version")
def make_lastest(modeladmin, request, queryset):
    if queryset.count() != 1:
        raise ValueError("Invalid number of version to make latest")
    
    version = queryset[0]
    service = VersionService(version)
    service.make_latest()
    

class VersionAdmin(admin.ModelAdmin):

    list_display = ("_version_name", "latest")
    actions = [make_lastest]

    def _version_name(self, obj):
        return str(obj)
    
    def save_model(self, request: HttpRequest, obj: Any, form: ModelForm, change: bool) -> None:
        service = VersionService(version=obj)
        service.save()


admin.site.register(Version, VersionAdmin)