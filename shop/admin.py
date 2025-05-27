from django.contrib import admin

from . models import Category, Mobile


@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    
@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display = ['name','category','inventory','price_main','price_with_discount','is_active','date_time_added',]