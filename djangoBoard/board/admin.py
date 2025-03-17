from django.contrib import admin
from .models import User, Category, Ad, Comment


class AdAdmin(admin.ModelAdmin):
    """Customizes the Ad Board view"""
    list_display = ["title", "created_at", "short_description", "comments_number", "is_active", "user", "price"]
    list_filter = ["created_at", "is_active", "user", "price", "category"]
    search_fields = ["title"]



class CategoryAdmin(admin.ModelAdmin):
    """Customizes the Category Board view"""
    list_display = ["name", "active_ads"]


class UserAdmin(admin.ModelAdmin):
    """Customizes the User Board view"""
    list_display = ["username", "ads_list"]





admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Comment)
