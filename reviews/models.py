from django.db import models


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    steam_app_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, default='Don\'t type this field.')
    review_summary = models.TextField()
    review_detail = models.TextField(blank=True)
    review_detail_link = models.CharField(max_length=255, blank=True)
    localized_by_developer = models.BooleanField()
    localized_by_community = models.BooleanField()
    published = models.BooleanField()
    invalid = models.BooleanField(default=True, editable=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
