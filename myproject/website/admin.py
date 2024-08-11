from django.contrib import admin
from .models import Member, Item, VariationImage, Review






# Register Member model
admin.site.register(Member)

class VariationImageInline(admin.TabularInline):
    model = VariationImage
    extra = 5  # Number of empty forms to display
    fields = ['image']  # Fields to display in the inline
    max_num = 10  # Maximum number of forms to display

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'old_price', 'discount_label')
    list_filter = ('discount_label',)
    search_fields = ('title', 'discount_label')
    fields = ('title', 'price', 'old_price', 'discount_label', 'image', 'image_hover')
    inlines = [VariationImageInline]  # Include the inline for variation images

    def save_model(self, request, obj, form, change):
        # Custom save method if needed
        super().save_model(request, obj, form, change)
        
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'item', 'rating', 'created_at')
    search_fields = ('name', 'email', 'item__name')
    list_filter = ('rating', 'created_at')

admin.site.register(Review, ReviewAdmin)