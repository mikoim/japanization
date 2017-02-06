from django.db import models


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    review_summary = models.TextField()
    review_detail_link = models.CharField(max_length=255)
    localized_by_developer = models.BooleanField()
    localized_by_community = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
