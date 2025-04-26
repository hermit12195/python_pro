from channels.db import database_sync_to_async

from blog.models import BlogUser

@database_sync_to_async
def get_email(username):
    user=BlogUser.objects.get(username=username)
    return user.email