from django.contrib import admin
from .models import Update, VersionUpdate
from .service import UpdateService


@admin.action(description="Run a update")
def run_update(modeladmin, request, queryset):
    if queryset.count() != 1:
        raise ValueError("Invalid number of update to run")
    
    update = queryset[0]
    service = UpdateService(update)
    service.run()

class VersionUpdateInline(admin.TabularInline):
    model = VersionUpdate
    extra = 1

class UpdateAdmin(admin.ModelAdmin):
    inlines = [VersionUpdateInline]
    actions = [run_update]
    

class VersionUpdateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Update, UpdateAdmin)
admin.site.register(VersionUpdate, VersionUpdateAdmin)
