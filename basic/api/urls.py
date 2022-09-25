from django.urls import path
from . import views

# jwt must be installed before using this.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)





urlpatterns = [
    
    # Will generate token for the authenticated user.
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # * Anytime the token expires a new to will be sent to the new user
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    
    
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),
]