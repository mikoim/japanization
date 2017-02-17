from django.views.generic import ListView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(ReadOnlyModelViewSet):
    queryset = Review.objects.filter(published=True, invalid=False)
    serializer_class = ReviewSerializer


class ReviewView(ListView):
    model = Review

    def get_queryset(self):
        return Review.objects.filter(published=True, invalid=False)
