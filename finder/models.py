from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower


class UserManager(BaseUserManager):
    """Create users that authenticate with an email address."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Application identity using unique email rather than a username."""

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ("first_name", "last_name", "email")
        indexes = [
            models.Index(
                fields=("first_name", "last_name", "email"),
                name="user_display_order_idx",
            )
        ]

    @property
    def display_name(self):
        full_name = self.get_full_name().strip()
        return full_name or self.email

    def __str__(self):
        return self.display_name


class StaffProfile(models.Model):
    """A browsable academic profile belonging to one staff user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    biography = models.TextField(
        max_length=1200,
        help_text="A short fictional biography shown to students.",
    )

    class Meta:
        ordering = ("user__first_name", "user__last_name", "user__email")

    @property
    def display_name(self):
        return self.user.display_name

    @property
    def initials(self):
        parts = [self.user.first_name, self.user.last_name]
        initials = "".join(part[0].upper() for part in parts if part)
        return initials or self.user.email[0].upper()

    def __str__(self):
        return self.display_name


class Interest(models.Model):
    """An area in which a staff member is willing to supervise work."""

    staff_profile = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="interests",
    )
    name = models.CharField(max_length=80)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(
                fields=("staff_profile", "name"),
                name="interest_owner_name_idx",
            )
        ]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "staff_profile",
                name="unique_interest_name_per_staff_ci",
            )
        ]

    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Enter an area of interest."})

    def __str__(self):
        return self.name


class ProjectIdea(models.Model):
    """A project proposal owned and maintained by one staff member."""

    staff_profile = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="project_ideas",
    )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)
        indexes = [
            models.Index(
                fields=("staff_profile", "title"),
                name="project_owner_title_idx",
            )
        ]

    def clean(self):
        self.title = self.title.strip()
        self.description = self.description.strip()
        errors = {}
        if not self.title:
            errors["title"] = "Enter a project title."
        if not self.description:
            errors["description"] = "Enter a project description."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title
