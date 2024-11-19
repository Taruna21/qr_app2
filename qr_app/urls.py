from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_generator/', include('qr_generator.urls')),
]
