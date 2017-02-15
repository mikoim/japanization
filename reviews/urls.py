from django.conf.urls import include, url
from django.views.generic import TemplateView, ListView, RedirectView
from rest_framework.routers import DefaultRouter

from .models import Review
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/sample')),
    url(r'^api/', include(router.urls)),
    url(r'^sample$', ListView.as_view(model=Review)),
    url(r'^edit$', TemplateView.as_view(template_name='reviews/edit.html')),
]
