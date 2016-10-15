from django.contrib import admin
from shortenersite.models import Urls, UserProfile


class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'http_url', 'org_date')
    ordering = ('-org_date',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_category')


admin.site.register(Urls, UrlsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

