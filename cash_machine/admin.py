from django.contrib import admin

from cash_machine.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price')
