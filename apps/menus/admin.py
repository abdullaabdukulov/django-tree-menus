from django.contrib import admin

from .models import MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    fk_name = "parent"
    extra = 0
    fields = ("name", "url", "order", "guid")
    readonly_fields = ("guid",)
    ordering = ("order",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_name", "parent", "url", "order", "guid")
    list_filter = ("menu_name",)
    search_fields = ("name", "url", "menu_name", "guid")
    inlines = [MenuItemInline]
    readonly_fields = ("guid", "created_time", "updated_time")
    fieldsets = (
        (None, {"fields": ("menu_name", "name", "url", "parent", "order")}),
        (
            "Metadata",
            {
                "fields": ("guid", "created_time", "updated_time"),
                "classes": ("collapse",),
            },
        ),
    )
