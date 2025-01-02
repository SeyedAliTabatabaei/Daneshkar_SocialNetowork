from django.urls import path
from . import views 

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/',views.profile_view,name='profile'),
    path('logout/',views.logout_view,name='logout'),
    path('write/',views.write_view,name='write'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('post/<int:pk>/delete/', views.delete_post, name='post_delete'),
    path('search/', views.search_users, name='search_users'),
    path('ajax/search-users/', views.ajax_search_users, name='ajax_search_users'),
    path('reaction/<int:post_id>/', views.reaction, name='reaction'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('followings/', views.followings, name='followings'),
]