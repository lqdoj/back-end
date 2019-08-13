import os
import time

from PIL import Image
from django.contrib.auth.models import User
from django.db import models

from lqdoj_backend.settings import AVATAR_FOLDER


def get_time_stamp():
    # Get the seconds since epoch
    seconds_since_epoch = time.time()
    # Convert seconds since epoch to struct_time
    time_obj = time.localtime(seconds_since_epoch)
    return '%d-%d-%d_%d-%d-%d' % (
        time_obj.tm_mday, time_obj.tm_mon, time_obj.tm_year, time_obj.tm_hour, time_obj.tm_min, time_obj.tm_sec)


def get_file_path(instance, filename):
    upload_to = os.path.join(AVATAR_FOLDER)
    extension = filename.split('.')[-1]
    filename = get_time_stamp() + "_" + instance.user.username
    final_filename = '{}.{}'.format(filename, extension)

    return os.path.join(upload_to, final_filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, to_field="username")
    avatar = models.ImageField(default='default.jpg', upload_to=get_file_path)

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
