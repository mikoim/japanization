from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
