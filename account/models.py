from django.db import models

from django.contrib.auth.models import AbstractUser,Group,Permission

# class CustomUser(AbstractUser):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#     ]
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

#     # Add related_name to avoid clashes with the default User model
#     groups = models.ManyToManyField(
#         Group,
#         blank=True,
#         related_name='customuser_set',
#         verbose_name=('groups'),
#         help_text=(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#     )
   
#     user_permissions = models.ManyToManyField(
#         Permission,
#         blank=True,
#         related_name='customuser_set',
#         verbose_name=('user permissions'),
#         help_text=('Specific permissions for this user.'),
#     )
    