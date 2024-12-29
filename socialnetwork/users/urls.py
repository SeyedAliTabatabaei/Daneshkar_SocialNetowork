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
]