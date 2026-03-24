from rest_framework import serializers

from .models import Book, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source="genre", write_only=True
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "owner",
            "title",
            "author",
            "genre",
            "genre_id",
            "condition",
            "type",
            "description",
            "image",
            "status",
            "share",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "genre", "created_at"]
