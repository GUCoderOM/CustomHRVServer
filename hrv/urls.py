from django.urls import path

from hrv import views
app_name = 'hrv' # ADDED
urlpatterns = [
    path('', views.index, name='index'),
    path('measures/', views.measures, name='measures'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<slug:username>',views.user, name = 'user'),
    path('register_watch/<username>',views.register_watch, name = 'register_watch'),
]
