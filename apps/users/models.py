from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


phone_validator = RegexValidator(
    regex=r"^\+?998\d{9}$",
    message="Phone number must be in the format +998XXXXXXXXX or 998XXXXXXXXX",
)


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("Telegram id kiritish majburiy")
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(telegram_id, password, **extra_fields)

    def get_by_natural_key(self, username):
        try:
            return self.get(**{self.model.USERNAME_FIELD: int(username)})
        except (ValueError, TypeError, self.model.DoesNotExist):
            raise self.model.DoesNotExist


class User(AbstractUser):
    username = None

    telegram_id = models.BigIntegerField(unique=True)
    phone = models.CharField(
        validators=[phone_validator], max_length=15, unique=True, null=True
    )
    name = models.CharField(max_length=64)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=0
    )
    telegram_username = models.CharField(
        max_length=64, null=True, blank=True, unique=True
    )

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def average_rating(self) -> float:
        """
        Calculates the average rating from all received reviews.
        """
        from django.db.models import Avg
        avg_rating = self.received_reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating, 1) if avg_rating else 0.0

    def update_rating(self) -> None:
        """
        Updates the stored rating based on average of received reviews.
        """
        self.rating = int(self.average_rating * 2)  # Scale to 0-10
        self.save(update_fields=['rating'])

    def __str__(self) -> str:
        return f"({self.telegram_id}) - {self.name}"
