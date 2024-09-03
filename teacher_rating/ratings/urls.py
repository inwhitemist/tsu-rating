from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, ActionViewSet, ReviewViewSet, add_action, action_success

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'actions', ActionViewSet)
router.register(r'reviews', ReviewViewSet)  # Добавлен маршрут для отзывов

urlpatterns = [
    path('api/', include(router.urls)),
    path('add_action/', add_action, name='add_action'),
    path('action_success/', action_success, name='action_success'),
]
