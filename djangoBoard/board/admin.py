"""Module for Django admin panel customization"""
from typing import List
from django.contrib import admin
from .models import User, Category, Ad, Comment
from userprofile.models import UserProfile


class AdAdmin(admin.ModelAdmin):
    """
    Customizes the Ad Board view in the Django admin interface.

    This class specifies the fields to be displayed in the list view,
    the filters to be applied, and the search fields available for searching ads.
    """
    list_display: List[str] = ["title", "created_at", "short_description", "comments_number", "is_active", "user",
                               "price"]
    list_filter: List[str] = ["created_at", "is_active", "user", "price", "category"]
    search_fields: List[str] = ["title"]


class CategoryAdmin(admin.ModelAdmin):
    """
    Customizes the Category Board view in the Django admin interface.

    This class defines the fields to display in the list view for categories,
    such as the name of the category and the number of active ads associated with it.
    """
    list_display: List[str] = ["name", "active_ads"]


class UserAdmin(admin.ModelAdmin):
    """
    Customizes the User Board view in the Django admin interface.

    This class specifies the fields to display in the list view for users,
    such as the username and a list of their ads.
    """
    list_display: List[str] = ["username", "ads_list", "id"]


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Comment)
admin.site.register(UserProfile)
