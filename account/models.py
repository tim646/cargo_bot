from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        CASHIER = "cashier", _("Cashier")
        MANAGER = "manager", _("Manager")
        ADMIN = "admin", _("Admin")
        OWNER = "owner", _("Owner")
        STAFF = "staff", _("Staff")

    phone_number = models.CharField(max_length=20, unique=True, verbose_name=_("Phone Number"))
    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    birth_date = models.DateField(verbose_name=_("Birth Date"))
    avatar = models.ImageField(upload_to="avatars/", verbose_name=_("Avatar"), blank=True, null=True)
    bio = models.TextField(verbose_name=_("Bio"), blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CASHIER, verbose_name=_("Role"))
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "full_name", "address", "birth_date"]
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name
