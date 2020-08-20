from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.success),
    path('logout', views.logout),
    path('create', views.create_books),
    path('update/<int:book_id>', views.update),
    path('books/<int:book_id>/delete', views.delete),
    path('books/<int:book_id>', views.detail),
    path('books/<int:book_id>/favorite', views.add_favorite),
    path('books/<int:book_id>/unfavorite', views.unfavorite),
]
