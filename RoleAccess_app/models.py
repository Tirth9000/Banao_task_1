from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=30)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    profile_pic = models.FileField(upload_to='media', blank=True)
    address_line = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=[('Dr', 'Doctor'), ('Pt', 'Patient')], default='Pt')

    def __str__(self):
        return self.role + " " + self.username

    def save(self, *args, **kwargs):
        # Check if password is already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)