from .models import Review
from rest_framework import serializers


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ('name', 'review_summary', 'review_detail_link', 'localized_by_developer', 'localized_by_community')
