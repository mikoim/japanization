from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(ReadOnlyModelViewSet):
    queryset = Review.objects.filter(published=True, invalid=False)
    serializer_class = ReviewSerializer
