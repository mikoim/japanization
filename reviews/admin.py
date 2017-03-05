from django.contrib import admin
from django.contrib import messages

from .models import Review
from .utils import SteamStore, SteamException


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'steam_app_id', 'name', 'localization_status', 'review_summary', 'review_detail', 'review_detail_link'
        'localized_by_developer', 'localized_by_community',
        'published', 'invalid'
    )

    list_filter = [
        'updated_at', 'localized_by_developer', 'localized_by_community', 'published', 'invalid'
    ]

    actions = ['mark_as_draft', 'mark_as_published', 'sync_with_steam']

    def mark_as_draft(self, request, queryset):
        rows_updated = queryset.update(published=False)
        if rows_updated == 1:
            message_bit = '1 review was'
        else:
            message_bit = '%s reviews were' % rows_updated
        self.message_user(request, '%s successfully marked as draft.' % message_bit)

    def mark_as_published(self, request, queryset):
        rows_updated = queryset.update(published=True)
        if rows_updated == 1:
            message_bit = '1 review was'
        else:
            message_bit = '%s reviews were' % rows_updated
        self.message_user(request, '%s successfully marked as published.' % message_bit)

    def sync_with_steam(self, request, queryset):
        store = SteamStore()
        success = 0

        for row in queryset:
            data = None
            app_id = row.steam_app_id

            try:
                data = store.appdetails(app_id)
            except SteamException as e:
                self.message_user(request, 'Steam AppID {:d} is invalid. ({:s})'.format(app_id, str(e)), messages.ERROR)
                row.invalid = True

            if data:
                row.name = store.name(data)
                if store.is_support_japanese(data):
                    row.localized_by_developer = True
                row.invalid = False
                success += 1

            row.save()

        if success >= 1:
            if success == 1:
                message_bit = '1 review was'
            else:
                message_bit = '%s reviews were' % success
            self.message_user(request, '%s successfully synced with Steam.' % message_bit)

admin.site.register(Review, ReviewAdmin)
