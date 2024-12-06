from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from device.views import DeviceViewSet
from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()
router.register(r'devices', DeviceViewSet, basename='devices')


urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
