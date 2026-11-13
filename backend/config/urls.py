from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Branding for the admin panel (replaces the default "Django administration").
admin.site.site_header = 'GuidedGlam'
admin.site.site_title = 'GuidedGlam'
admin.site.index_title = 'Site administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('catalog.urls')),
    path('api/', include('social.urls')),
]

# While developing, let Django hand out uploaded photos itself.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
