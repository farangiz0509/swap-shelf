from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SwapRequest, Swap
from .serializers import SwapRequestSerializer, SwapSerializer


class SwapRequestViewSet(viewsets.ModelViewSet):
    queryset = SwapRequest.objects.select_related("book", "requester").all()
    serializer_class = SwapRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        swap_request = self.get_object()
        if swap_request.book.owner != request.user:
            return Response({"error": "Only book owner can accept"}, status=status.HTTP_403_FORBIDDEN)
        if swap_request.status != SwapRequest.Status.PENDING:
            return Response({"error": "Request already processed"}, status=status.HTTP_400_BAD_REQUEST)

        swap_request.status = SwapRequest.Status.ACCEPTED
        swap_request.save()

        # Create swap
        swap = Swap.objects.create(
            book=swap_request.book,
            owner=swap_request.book.owner,
            borrower=swap_request.requester,
            type=swap_request.book.type
        )

        # Update book status
        swap_request.book.status = "unavailable"
        swap_request.book.save()

        return Response({"message": "Request accepted", "swap_id": swap.id})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        swap_request = self.get_object()
        if swap_request.book.owner != request.user:
            return Response({"error": "Only book owner can reject"}, status=status.HTTP_403_FORBIDDEN)

        swap_request.status = SwapRequest.Status.REJECTED
        swap_request.save()
        return Response({"message": "Request rejected"})


class SwapViewSet(viewsets.ModelViewSet):
    queryset = Swap.objects.select_related("book", "owner", "borrower").all()
    serializer_class = SwapSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def mark_returned(self, request, pk=None):
        swap = self.get_object()
        if swap.borrower != request.user:
            return Response({"error": "Only borrower can mark as returned"}, status=status.HTTP_403_FORBIDDEN)

        swap.status = Swap.Status.COMPLETED
        swap.save()

        # Update book status
        swap.book.status = "available"
        swap.book.save()

        return Response({"message": "Marked as returned"})

    @action(detail=True, methods=['post'])
    def confirm_return(self, request, pk=None):
        swap = self.get_object()
        if swap.owner != request.user:
            return Response({"error": "Only owner can confirm return"}, status=status.HTTP_403_FORBIDDEN)

        swap.status = Swap.Status.COMPLETED
        swap.save()

        # Update book status
        swap.book.status = "available"
        swap.book.save()

        return Response({"message": "Return confirmed"})
