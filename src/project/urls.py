from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from apps.contact.views import ContactView

urlpatterns = [
    path('', ContactView.as_view(), name='home'),
    path('thanks/', TemplateView.as_view(template_name='contact/thanks.html'), name='home'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # pragma: no cover
    # Add django-debug-toolbar URLs
    if settings.DEBUG_TOOLBAR:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    # Serve media root only in DEBUG mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
