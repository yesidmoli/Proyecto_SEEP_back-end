from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

from rest_framework.permissions import BasePermission
class UserManager(BaseUserManager):

    def create_user(self, documento, password, name,   rol, **extra_fields):
        if not documento:
            raise ValueError('Falta el documento')
        user =self.model(documento = documento, name=name , rol = rol,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,documento, password, name,   rol = 'admin' , ):
        user = self.create_user( documento, password, name,  rol =rol )
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('instructor', 'Instructor'),
        ('aprendiz', 'Aprendiz'),
        ('admin', 'Admin'),
    )

    email = models.EmailField()
    name = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=ROLES)
    documento = models.CharField(max_length=20, unique=True) 
    is_staff = models.BooleanField(default =False)
    is_active = models.BooleanField(default=True)
    must_change_password = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.get_username()
    
    def get_username(self):
        """Return the username for this User."""
        return getattr(self, 'documento')


class IsInstructor(BasePermission):

    def has_permission(self, request, view):
        return request.user.rol == 'instructor'

class IsAprendiz(BasePermission):

    def has_permission(self, request, view):
        return request.user.rol == 'aprendiz'
    
