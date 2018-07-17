"""bms_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app01 import views

urlpatterns = [
    path('login/', views.login),
    path('logout/',views.logout),
    path('register/',views.register),
    re_path('publisher_list/', views.publisher_list,name='publisher_list'),
    re_path('add_publisher/',views.add_publisher,name='add_publisher'),
    re_path('delete_publisher/(?P<del_id>\d+)',views.delete_publisher,name='delete_publisher'),
    re_path('edit_publisher/(?P<ed_id>\d+)',views.edit_publisher,name='edit_publisher'),

    re_path('author_list/',views.author_list,name='author_list'),
    re_path('add_author/',views.add_author,name='add_author'),
    re_path('delete_author/(?P<del_id>\d+)',views.delete_author,name='delete_author'),
    re_path('edit_author/(?P<ed_id>\d+)',views.edit_author,name='edit_author'),

    re_path('add_book/', views.add_book, name='add_book'),
    re_path('delete_book/(?P<del_id>\d+)', views.delete_book, name='delete_book'),
    re_path('edit_book(?P<ed_id>\d+)', views.edit_book, name='edit_book'),
    re_path('', views.book_list, name='book_list'),
]
