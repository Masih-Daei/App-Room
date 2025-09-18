from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<int:pk>',views.room,name='room'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<int:pk>',views.updateRoom,name = 'update-room'),
    path('delete-room/<int:pk>',views.deleteRoom,name = 'delete-room'),
    path('login/',views.loginPage,name ='login'),
    path('logout/',views.logoutPage,name ='logout'),
    path('register/',views.registerPage,name ='register'),
    path('delete-message/<int:pk>',views.deleteMessage,name = 'delete-message'),
    path('profile/<int:pk>',views.userProfile,name='user-profile'),
    path('topics/',views.topicsPage,name='topics'),
    path('activity/',views.activity_Page,name='activity'),
    path('update-user/',views.updateUser,name='update-user')
]