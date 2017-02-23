from rest_framework.serializers import ModelSerializer

from .models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'steam_app_id', 'name',
            'review_summary', 'review_detail', 'review_detail_link',
            'localization_status', 'localized_by_developer', 'localized_by_community'
        )
