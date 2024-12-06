from django.contrib import admin
from .models import Update, VersionUpdate
from .service import UpdateService
from django.contrib import messages


@admin.action(description="Run a update")
def run_update(modeladmin, request, queryset):
    if queryset.count() != 1:
        raise ValueError("Invalid number of update to run")
    
    update = queryset[0]
    service = UpdateService(update)
    service.run()
    messages.add_message(request, messages.SUCCESS, "The update was send.")

class VersionUpdateInline(admin.TabularInline):
    model = VersionUpdate
    extra = 1


class UpdateAdmin(admin.ModelAdmin):
    inlines = [VersionUpdateInline]
    actions = [run_update]

    def save_model(self, request, obj, form, change):
        service = UpdateService(obj)
        service.save()


class VersionUpdateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Update, UpdateAdmin)
admin.site.register(VersionUpdate, VersionUpdateAdmin)
