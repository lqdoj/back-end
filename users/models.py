from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username")
    avatar = models.ImageField(default='default.jpg', upload_to='avatars')

    def __str__(self):
        return "User profile: " + self.user.username

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        img = Image.open(self.avatar.path)
        if (img.height > 150) or (img.width > 150):
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
