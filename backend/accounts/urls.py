#accounts/urls.py 
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')


role_router = DefaultRouter()
role_router.register(r'', RoleViewSet, basename='role')


urlpatterns = [
    path('', include(router.urls)),
]
