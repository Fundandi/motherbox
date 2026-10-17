from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

admin.site.site_header = 'Motherbox administration'
admin.site.site_title = 'Motherbox'
admin.site.index_title = 'Drift'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('orders.urls')),
    path('', include('catalog.urls')),
]
