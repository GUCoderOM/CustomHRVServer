from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from hrv import views
app_name = 'hrv' # ADDED
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<slug:username>',views.user, name = 'user'),
    path('register_watch/<username>',views.register_watch, name = 'register_watch'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]
