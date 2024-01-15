
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('', include('Quiz.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
