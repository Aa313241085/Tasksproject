from django.urls import path

from . import views

urlpatterns = [
    path("create-user/", views.create_user, name = "create_user"),
    path("login/", views.login, name = "login"),
    path("logout/", views.logout, name = "logout"),
    path("", views.home, name = "home"),
    path("create/", views.create_task, name = "create_task"),
    path("delete/<int:id>/", views.delete, name = "delete"),
    path("update/<int:id>/", views.update, name ='update'),
    path("search/", views.search, name = "search"),
    path("show_user/", views.show_user, name = "show_user"),
    path("delete_user/<int:id>/", views.delete_user, name = "delete_user")
]
