from django.contrib import admin

from marketplace.apps.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'email',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'email',
        'last_name',
        'name'
    ]

    list_per_page = 30
    list_max_show_all = 30
