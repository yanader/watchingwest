from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class User(models.Model):
    pass


class Opponent(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=8, default="", blank=True)

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    title=models.CharField(max_length=64)
    photo=models.ImageField(upload_to="pics")

    def image_tag(self): # new
        return mark_safe(
            f'<img src="{self.photo.url}" style="max-width: 40%; height: auto;" />'
        )
    
class Competition(models.Model):
    competition = models.CharField(max_length=64, default="", blank=True)

    def __str__(self):
        return f"{self.competition}"


class Entry(models.Model):
    opponent = models.ForeignKey(Opponent, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    location = models.CharField(max_length=64)
    home = models.BooleanField(default=True)
    text_entry = models.CharField(max_length=400)
    image = models.OneToOneField(Image, null=True, blank=True, on_delete=models.SET_NULL)
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.date} - {self.opponent}"

class PasswordEntry(models.Model):
    password = models.CharField(max_length=64)