from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        """Create and save a User with the given email/phone and password."""
        if email:
            email = self.normalize_email(email)
        user = self.model(
            username=username, email=email or None, phone=phone or None, **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, phone=None, password=None, **extra_fields):
        """Create and save a regular User with the given email/phone and password."""
        if not any([email, phone]):
            raise ValueError("email or phone must be set")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, phone, password, **extra_fields)

    def create_superuser(
        self, username=None, email=None, phone=None, password=None, **extra_fields
    ):
        """Create and save a super user."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, phone, password, **extra_fields)
