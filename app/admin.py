from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Contact, Game, Platform, PlayStyle, Follow, Post


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dane osobiste', {'fields': ('name', 'username', 'bio', 'avatar', 'background')}),
        ('Uprawnienia', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'username')
    ordering = ('email',)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_form', 'contact_username', 'contact_link')
    search_fields = ('user__email', 'contact_form', 'contact_username')
    list_filter = ('user', 'contact_form')


class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_name')
    search_fields = ('user__email', 'game_name')
    list_filter = ('user', 'game_name')


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform_name')
    search_fields = ('user__email', 'platform_name')
    list_filter = ('user', 'platform_name')


class PlayStyleAdmin(admin.ModelAdmin):
    list_display = ('user', 'play_style_name')
    search_fields = ('user__email', 'play_style_name')
    list_filter = ('user', 'play_style_name')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed_user')
    search_fields = ('follower__email', 'followed_user__email')
    list_filter = ('follower', 'followed_user')


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')
    search_fields = ('user__email', 'text')
    list_filter = ('user', 'created_at')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(PlayStyle, PlayStyleAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Post, PostAdmin)
