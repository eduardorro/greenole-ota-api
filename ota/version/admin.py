from django.contrib import admin
from .models import Version


class VersionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Version, VersionAdmin)