from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from faculty.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parents/', include('parents.urls', namespace='parents')),
    path('', include('students.urls', namespace='students')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )