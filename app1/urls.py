from django.urls import path

from app1 import views

app_name = 'app1'

urlpatterns = [
    path("user/", views.user, name='user'),
    path("user_view/", views.UserView.as_view(), name='user_view'),
    path("student/", views.StudentView.as_view(), name='student'),
    path("student/<str:id>/", views.StudentView.as_view(), name='student'),
]

