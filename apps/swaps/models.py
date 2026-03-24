from django.db import models
from django.utils import timezone

from apps.books.models import Book
from apps.users.models import User


class SwapRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    book = models.ForeignKey(Book, related_name="swap_requests", on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.book.title} by {self.requester.phone}"


class Swap(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    book = models.ForeignKey(Book, related_name="swaps", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="owned_swaps", on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, related_name="borrowed_swaps", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[("borrow", "Borrow"), ("permanent", "Permanent")])
    status = models.CharField(choices=Status.choices, default=Status.ACTIVE)
    return_deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Swap of {self.book.title} from {self.owner.phone} to {self.borrower.phone}"
