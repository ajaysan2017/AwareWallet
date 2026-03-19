from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets, permissions
from .models import RecurringTransaction
from .serializers import RecurringTransactionSerializer

class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

router = DefaultRouter()
router.register(r'', RecurringTransactionViewSet, basename='api-recurring')
urlpatterns = router.urls