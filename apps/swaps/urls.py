from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SwapRequestViewSet, SwapViewSet

router = DefaultRouter()
router.register(r"swap-requests", SwapRequestViewSet, basename="swap-request")
router.register(r"swaps", SwapViewSet, basename="swap")

urlpatterns = router.urls
