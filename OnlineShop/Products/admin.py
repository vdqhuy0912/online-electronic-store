from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductPhotosInline(admin.TabularInline):
    model = ProductPhotos
    raw_id_fields = ['product']


class ProductAdminForm(forms.ModelForm):
    characteristics = forms.CharField(widget=CKEditorUploadingWidget())
    info = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(ProductSubcategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'main_category']
    list_display_links = ['id', 'name']
    list_editable = ['main_category']
    search_fields = ['name', 'main_category']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['id', 'name', 'main_category', 'subcategory', 'article', 'status']
    list_display_links = ['id', 'name', 'article']
    list_filter = ['main_category', 'subcategory', 'status']
    list_editable = ['main_category', 'subcategory', 'status']
    search_fields = ['name', 'article']
    inlines = [ProductPhotosInline]
    exclude = ['editing']


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']
    search_fields = ['id']


@admin.register(ProductMemoryCategory)
class ProductMemoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'memory_size']
    list_display_links = ['id', 'memory_size']
    search_fields = ['id', 'memory_size']
    exclude = ['memory_size']



@admin.register(ProductColorCategory)
class ProductColorCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'color_in_admin_panel']
    list_display_links = ['id', 'color_in_admin_panel']
    search_fields = ['id', 'color_in_admin_panel']
