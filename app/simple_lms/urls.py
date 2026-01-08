"""
URL configuration for simple_lms project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from ninja import NinjaAPI
from lms.api import router as lms_router

# Inisialisasi API
api = NinjaAPI(title="Simple LMS API")

# Sesuai UAS: prefix /api/lms/...
api.add_router("/lms", lms_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

# Serve media files in development (DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
