from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start, name='start'),
    path('pakker/', views.package_list, name='package_list'),
    path('pakker/<slug:slug>/', views.package_detail, name='package_detail'),
    path('producenter/', views.manufacturer_list, name='manufacturer_list'),
    path('producenter/<slug:slug>/', views.manufacturer_detail, name='manufacturer_detail'),
    path('videnskaben/', views.science, name='science'),
    path('om-os/', views.page, {'template': 'about'}, name='about'),
    path('faq/', views.page, {'template': 'faq'}, name='faq'),
    path('handelsbetingelser/', views.page, {'template': 'terms'}, name='terms'),
    path('privatlivspolitik/', views.page, {'template': 'privacy'}, name='privacy'),
    path('fortrydelsesret/', views.page, {'template': 'withdrawal'}, name='withdrawal'),
]
