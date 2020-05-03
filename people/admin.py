from django.contrib import admin
from .models import Person, Job, Crowd

# Register your models here.
admin.site.register(Job)
admin.site.register(Crowd)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  list_display = ('name', 'job')



# from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericTabularInline

# from myproject.myapp.models import Image, Product

# class ImageInline(GenericTabularInline):
#     model = Image

# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         ImageInline,
#     ]

# admin.site.register(Product, ProductAdmin)