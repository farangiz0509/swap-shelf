from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.swaps.models import Swap
from apps.users.models import User


class Review(models.Model):
    swap = models.ForeignKey(Swap, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name="given_reviews", on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(User, related_name="received_reviews", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        # Update the reviewed user's rating
        self.reviewed_user.update_rating()

    def __str__(self) -> str:
        return f"Review by {self.reviewer.name} for {self.reviewed_user.name} - {self.rating}/5"
