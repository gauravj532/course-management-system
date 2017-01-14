
from django.conf.urls import url,include
from django.contrib import admin
from studentix.admin import admin_site

urlpatterns = [
    url(r'^admin/', admin_site.urls),
    url(r'^studentix/', include('studentix.urls')),
]
