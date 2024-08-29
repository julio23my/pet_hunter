import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from users.managers import RegularManager, VeterinarianManager


class User(AbstractUser):
    class Types(models.TextChoices):
        REGULAR = "REG", "Regular"
        VET = "VET", "Veterinarian"
        

    base_type = Types.REGULAR

    # What type of user are we?
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    # First Name and Last Name Do Not Cover Name Patterns
    # Around the Globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
   

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)


class Regular(User):
    base_type = User.Types.REGULAR
    objects = RegularManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "whisper"


class VeterinarianMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    graduation_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.datetime.now().year)
        ]
    )
    specialization = models.CharField(max_length=255)
    is_specialized = models.BooleanField(default=False)
    takes_emergencies = models.BooleanField(default=False)    


class Veterinarian(User):
    base_type = User.Types.VET
    objects = VeterinarianManager()

    class Meta:
        proxy = True