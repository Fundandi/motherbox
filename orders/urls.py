from django.urls import path

from . import views

urlpatterns = [
    path('bestil/tak/', views.checkout_success, name='checkout_success'),
    path('bestil/demo/<str:reference>/', views.checkout_demo, name='checkout_demo'),
    path('bestil/annulleret/<str:reference>/', views.checkout_cancel, name='checkout_cancel'),
    path('bestil/<slug:slug>/', views.checkout, name='checkout'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('mit-abonnement/', views.manage_subscription, name='manage_subscription'),
    path('fortryd-aftale/', views.withdraw, name='withdraw'),
]
