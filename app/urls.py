from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.start_view, name='start'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/', views.feed_view, name='home'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit_user/', views.edit_user_view, name='edit_user'),
    path('edit_contacts_list/', views.edit_contacts_list_view, name='edit_contacts_list'),
    path('delete_contact/<int:contact_id>/', views.delete_contact_view, name='delete_contact'),
    path('edit_contact/<int:contact_id>/', views.edit_contact_view, name='edit_contact'),
    path('edit_games/', views.edit_games_view, name='edit_games'),
    path('edit_platforms/', views.edit_platforms_view, name='edit_platforms'),
    path('edit_play_styles/', views.edit_play_styles_view, name='edit_play_styles'),
    path('delete_game/<int:game_id>/', views.delete_game_view, name='delete_game'),
    path('delete_platform/<int:platform_id>/', views.delete_platform_view, name='delete_platform'),
    path('delete_play_style/<int:play_style_id>/', views.delete_play_style_view, name='delete_play_style'),
    path('find_partner/', views.find_partner_view, name='find_partner'),
    path('follow/<str:user_id>', views.follow_view, name='follow'),
    path('friends/', views.friends_view, name='friends'),
    path('friends/following', views.following_view, name='following'),
    path('friends/followers', views.followers_view, name='followers'),
    path('delete_post/<int:post_id>/', views.delete_post_view, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
