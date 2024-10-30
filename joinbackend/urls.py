from django.contrib import admin
from django.urls import path
from join.views import LoginView, UserCreate, ContactView, TaskView, GuestLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', UserCreate.as_view()),
    path('contacts/', ContactView.as_view()),
    path('contacts/<int:pk>/', ContactView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/', TaskView.as_view()),
    path('guest_login/', GuestLoginView.as_view())
]
