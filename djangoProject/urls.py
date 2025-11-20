from django.contrib import admin
from django.urls import path, include
from cases.views import HomeView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('cases.urls', 'cases'), namespace='cases')),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),


    
   

]
