from django.contrib import admin
from .models import Category, Product, Order
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'old_price', 'date_created')
    list_per_page = 50
    ordering = ['-date_created']
    search_fields = ['name, description', 'meta_keywords',]
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.image.url))
    image_preview.short_description = 'Product Image Preview'
    readonly_fields = ['image_preview']

class CategoryAdmin(admin.ModelAdmin):
    list_dsiplay = ('name', 'date_created', 'last_updated')
    list_per_page = 20
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug': ('name',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'phone', 'product', 'quantity', 'address', 'date_ordered']
    search_fields = ['customer', 'address', ]
    actions = ['mark_as_complete', 'mark_as_pending']

    def mark_as_complete(self, request, queryset):
        queryset.update(order_complete=True)

    def mark_as_pending(self, request, queryset):
        queryset.update(order_complete=False)
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)

admin.site.site_header = "DukaOnline Admin Dashboard"
admin.site.site_title = "DukaOnline"
admin.site.index_title = "Welcome to DukaOnline Admin Dashboard"
