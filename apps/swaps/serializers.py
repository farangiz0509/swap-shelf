from rest_framework import serializers

from .models import SwapRequest, Swap


class SwapRequestSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    requester_phone = serializers.CharField(source="requester.phone", read_only=True)

    class Meta:
        model = SwapRequest
        fields = ["id", "book", "book_title", "requester", "requester_phone", "message", "status", "created_at"]
        read_only_fields = ["id", "requester", "created_at"]


class SwapSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    owner_phone = serializers.CharField(source="owner.phone", read_only=True)
    borrower_phone = serializers.CharField(source="borrower.phone", read_only=True)

    class Meta:
        model = Swap
        fields = ["id", "book", "book_title", "owner", "owner_phone", "borrower", "borrower_phone", "type", "status", "return_deadline", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]
