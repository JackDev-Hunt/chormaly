from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('extract/', views.extract_colors, name='extract_colors'),
    path('about/', views.about, name='about'),
    path('api/track-ad-click/', views.track_ad_click, name='track_ad_click'),
    
    
    
]