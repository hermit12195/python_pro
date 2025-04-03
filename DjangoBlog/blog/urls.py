from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    path("login/", views.signin, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<str:username>/", views.feed, name="feed"),
    path("<str:username>/profile/", views.create_profile, name="profile"),
    path("<str:username>/edit_profile/", views.edit_profile, name="edit_profile"),
    path("<str:username>/create_post/", views.create_post, name="create_post"),
    path("<str:username>/<int:id>/", views.post_detail, name="post_details"),
    path("<str:username>/my_posts/", views.my_posts, name="my_posts"),
    path("<str:username>/<int:id>/edit_post/", views.edit_post, name="edit_post"),
    path("<str:username>/<int:id>/delete_post/", views.delete_post, name="delete_post"),
    path("<str:username>/<int:id>/comment/", views.comment, name="comment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
