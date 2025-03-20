"""Module for Django views"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Ad, Category, Comment


def admin_stats(request: HttpRequest) -> HttpResponse:
    """
    Generates and renders statistical data for ads and comments in different categories.

    The function calculates:
    - The total number of ads in each category.
    - The number of active and inactive ads per category.
    - The number of comments associated with ads in each category.
    - A total row summarizing all ads and comments.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'admin_stats.html' template with statistical data.

    """
    categ_details, categories = {}, {}
    for category in Category.objects.all():
        comments_num = 0
        for ad in [comment.ad.all() for comment in Comment.objects.all()]:
            get_ad = Ad.objects.get(title=ad.first())
            if get_ad.category.first() == category:
                comments_num += 1
        categories[category.name] = {
            "ads_number": Ad.objects.filter(category=category).count(),
            "active_ads": Ad.objects.filter(category=category, is_active=True).count(),
            "inactive_ads": Ad.objects.filter(category=category, is_active=False).count(),
            "comment_num": comments_num
        }
    ads_number, active_ads, inactive_ads, comment_num = 0, 0, 0, 0
    for categ_dict in categories.values():
        ads_number += int(categ_dict["ads_number"])
        active_ads += int(categ_dict["active_ads"])
        inactive_ads += int(categ_dict["inactive_ads"])
        comment_num += int(categ_dict["comment_num"])
    categories["Total"] = {
        "ads_number": ads_number,
        "active_ads": active_ads,
        "inactive_ads": inactive_ads,
        "comment_num": comment_num
    }
    return render(request, "board/admin_stats.html", {"categories": categories,
                  "categories_names": ["Number of Ads", "Number of Active Ads", "Number of Deactivated Ads", "Number of comments"]})
