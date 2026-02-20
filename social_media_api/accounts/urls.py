from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FeedView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('feed/', FeedView.as_view()),
    *router.urls,
]
