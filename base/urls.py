from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    
    # leave store API endpoints at root level
    path('api/', include('store.api_urls')),  # ⬅️ you'll create this (see below)
    
    # only include other app routes if you still need them
    path('api/cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
