from django.contrib import admin
from .models import Member
from .models import Item





 
admin.site.register(Member)

@admin.register(Item)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'old_price', 'discount_label')
    list_filter = ('discount_label',)
    search_fields = ('title', 'discount_label')
    fields = ('title', 'price', 'old_price', 'discount_label', 'image', 'image_hover')

    def save_model(self, request, obj, form, change):
        # Custom save method if needed
        super().save_model(request, obj, form, change)

