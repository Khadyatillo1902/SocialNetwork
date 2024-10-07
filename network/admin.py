from django.contrib import admin
from .models import User, Post, Follow, Comment

class LikesAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes",)

admin.site.register(User)
admin.site.register(Post, LikesAdmin)
admin.site.register(Follow)
admin.site.register(Comment)
