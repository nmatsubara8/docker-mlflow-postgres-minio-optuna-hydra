from django.urls import path
from viewer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("search/", views.search, name="search"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
