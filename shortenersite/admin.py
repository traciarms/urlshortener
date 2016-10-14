from django.contrib import admin
from shortenersite.models import Urls


class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'http_url', 'org_date')
    ordering = ('-org_date',)


admin.site.register(Urls, UrlsAdmin)

