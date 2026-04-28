# config/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    path('api/v1/users/', include('accounts.urls')),
    path('api/v1/roles/', include('accounts.urls_roles')),
    # path('api/v1/customers/', include('customers.urls')),
    # path('api/v1/products/', include('products.urls')),
    # path('api/v1/inventory/', include('inventory.urls')),
    # path('api/v1/orders/', include('orders.urls')),
    # path('api/v1/production/', include('production.urls')),
    # path('api/v1/finance/', include('finance.urls')),
    # path('api/v1/reports/', include('reports.urls')),

]
# API Documentation
urlpatterns += [
    # YOUR PATTERNS
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


