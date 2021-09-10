from django.contrib import admin
from .models import Category, Product
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    # fields that can be edit in admin list view
    list_editable = ['price', 'available']
    # use the prepopulated_fields attribute to specify fields where the value is automatically set using
    # the value of other fields. As you have seen before, this is convenient for generating slugs.
    prepopulated_fields = {'slug': ('name',)}
