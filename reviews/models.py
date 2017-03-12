from django.db import models


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    steam_app_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True, default='!!! DON\'T TOUCH !!!',
                            help_text='This field will be filled automatically by synchronizing with Steam.')
    localization_status = models.TextField(blank=True)
    review_summary = models.TextField()
    review_detail = models.TextField(blank=True)
    review_detail_link = models.CharField(max_length=255, blank=True)
    localized_by_developer = models.BooleanField(default=False)
    localized_by_community = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    invalid = models.BooleanField(default=True, editable=False)

    class Meta(object):
        ordering = ('name',)

    def __str__(self):
        return self.name
