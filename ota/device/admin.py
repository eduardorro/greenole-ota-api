from django.contrib import admin
from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("_device_name", "_version_name")

    def _device_name(self, obj):
        return str(obj)
    
    def _version_name(self, obj):
        return str(obj.version) if obj.version else "-"


admin.site.register(Device, DeviceAdmin)