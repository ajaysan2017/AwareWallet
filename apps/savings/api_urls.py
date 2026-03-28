from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets, permissions
from .models import SavingsGoal
from .serializers import SavingsGoalSerializer

class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

router = DefaultRouter()
router.register(r'', SavingsGoalViewSet, basename='api-savings')
urlpatterns = router.urls
