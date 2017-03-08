from django.conf.urls import include, url
from django.views.decorators.cache import cache_page as cp
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, ReviewView

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    url(r'^$', cp(60 * 5)(ReviewView.as_view(template_name='reviews/index_list.html')), name='reviews-index'),
    url(r'^api/', include(router.urls), name='reviews-api'),
    url(r'^manual$', cp(60 * 60)(ReviewView.as_view(template_name='reviews/manual.html')), name='reviews-manual'),
    url(r'^sample$', cp(60 * 5)(ReviewView.as_view(template_name='reviews/sample_list.html')), name='reviews-sample'),
    url(r'^edit$', TemplateView.as_view(template_name='reviews/edit.html'), name='reviews-edit'),
]
