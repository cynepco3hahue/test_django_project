from django.contrib import admin
from log_collector.models import Log, Host


class LogAdmin(admin.ModelAdmin):
    search_fields = ['log_name']
    list_filter = ['log_name']
    list_display = ('log_name', 'log_path')

admin.site.register(Log, LogAdmin)
admin.site.register(Host)