from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_phone = serializers.CharField(source="reviewer.phone", read_only=True)
    reviewed_user_phone = serializers.CharField(source="reviewed_user.phone", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "swap", "reviewer", "reviewer_phone", "reviewed_user", "reviewed_user_phone", "rating", "comment", "created_at"]
        read_only_fields = ["id", "reviewer", "created_at"]
