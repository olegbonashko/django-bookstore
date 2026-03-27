from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace="catalog")),
    path("users/", include("users.urls", namespace="users")),
    path('__debug__/', include(debug_toolbar.urls)),
]