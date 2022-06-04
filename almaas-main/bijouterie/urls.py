from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

# directions à partir de admin ( importé plus haut, multitude de chemins réglables offerts par le framework)

    path("admin/", admin.site.urls),

    # chemins que nous avons crées dans notre appli store

    path("", include("store.urls")),

    # Chemins pour effectuer des payements

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
