from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from wagtail.documents import urls as wagtaildocs_urls
from django.conf.urls.i18n import i18n_patterns

# Use i18n_patterns to prefix URLs with language codes
urlpatterns = i18n_patterns(
    # Admin
    path("django-admin/", admin.site.urls),
    path('rosetta/', include('rosetta.urls')),  # Add Rosetta here
    path("admin/", include(crx_admin_urls)),
    # Documents
    path("docs/", include(wagtaildocs_urls)),
    # Search
    path("search/", include(crx_search_urls)),
    # For page serving
    path("", include(crx_urls)),
)

# Additional settings for DEBUG mode
if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # type: ignore
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
