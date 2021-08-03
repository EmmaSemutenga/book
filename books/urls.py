from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path('books/', views.BookList.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookView.as_view(), name='book_view'),
    path('new/', views.BookCreate.as_view(), name='book_new'),
    path('edit/<int:pk>/', views.BookUpdate.as_view(), name='book_edit'),
    path('delete/<int:pk>/', views.BookDelete.as_view(), name='book_delete'),
]

