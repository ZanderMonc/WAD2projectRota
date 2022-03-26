from django.urls import path, include
from rota import views

app_name = 'rota'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('timetable/', views.T.as_view(), name='timetable'),
    path('shift/new/', views.shift, name='shift_new'),
    path('shift/edit/<shift_id>/', views.shift, name='shift_edit'),
]
