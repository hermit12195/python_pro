from django.contrib import admin
from typing import List
from .models import *


class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Post objects.

    Attributes:
        list_display (List[str]): Fields to display in the list view.
        list_filter (List[str]): Fields to filter the list view by.
        search_fields (List[str]): Fields to search by in the list view.
    """
    list_display: List[str] = ["title", "created_datetime", "is_active", "user"]
    list_filter: List[str] = ["created_datetime", "is_active", "user"]
    search_fields: List[str] = ["title"]


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Category objects.

    Attributes:
        list_display (List[str]): Fields to display in the list view.
    """
    list_display: List[str] = ["title", "active_posts"]


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Profile objects.

    Attributes:
        list_display (List[str]): Fields to display in the list view.
    """
    list_display: List[str] = ["user"]


admin.site.register(BlogUser)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
