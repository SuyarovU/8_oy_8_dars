from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('tasks/', views.TodoView.as_view()),
    path('tasks/<int:pk>/', views.TodoDetailView.as_view()),
    path("auth/login/", views.CustomLoginView.as_view(), name='jwt login'),
    path("auth/refresh/", TokenRefreshView.as_view(), name='refresh-jwt'),
    path("auth/register/", views.RegisterView.as_view()),
    path('auth/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('auth/docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
]
