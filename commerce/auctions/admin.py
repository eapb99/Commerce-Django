from django.contrib import admin

# Register your models here.
from auctions.models import *


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information', {'fields': ('username', 'password', 'email')}),
    )

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Required Information', {'fields': ('name', 'image')}),
        ('Optional', {'fields': ('code', 'description')})
    )


class ListingAdmin(admin.ModelAdmin):
    list_display = ['lis_name', 'lis_price',  'lis_user', 'get_categories']
    fieldsets = (
        ('Details', {'fields': (('lis_name', 'lis_price'), 'lis_description', 'lis_image')}),
        ('Relational Information', {'fields': ('watchlist', 'category', 'lis_user')})
    )
    filter_horizontal = ('category', 'watchlist')


class CommentAdmin(admin.ModelAdmin):
    #list_display = ['user', 'listings']
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid)
admin.site.register(Listing,ListingAdmin)

