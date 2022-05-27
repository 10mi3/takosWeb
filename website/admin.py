from django.contrib import admin
from .models import (Image, Gallery, Pro, Actualites, Service,Contact, Item, Order, Category, Criteria, Aboutus)


# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(Aboutus)
class AboutusAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Pro)
class ProAdmin(admin.ModelAdmin):
    # list_display = ('name', 'desc', 'created_by', 'tools',)
    pass


@admin.register(Actualites)
class ActualiteAdmin(admin.ModelAdmin):
    # list_display = ('name', 'desc', 'ev_date',)
    pass



@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    # list_display = ('image', 'desc',)
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # list_display = ('name', 'ev_date',)
    pass
