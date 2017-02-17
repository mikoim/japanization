from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'updated_at', 'steam_app_id', 'name', 'localized_by_developer', 'localized_by_community', 'published', 'invalid'
    )
    list_filter = [
        'updated_at', 'localized_by_developer', 'localized_by_community', 'published', 'invalid'
    ]
admin.site.register(Review, ReviewAdmin)
