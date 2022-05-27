from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,email,password = None):
        if username is None:
            raise TypeError("User must have username")
        if email is None:
            raise TypeError("User must have email ")
        # define how user should be created
        user = self.model(username = username, email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password = None):
        if password is None:
            raise TypeError("Password field must be filled")
        user = self.create_user(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save() 
        return user

# give access to regular user field
class User(AbstractBaseUser,PermissionsMixin):
    # use db_index=True when you have a field that is unique for more useful lookups. 
    # if not unique you will get probably recieve multiple results from your queries and this might not be as useful as using an referencing their id.
    # Without db_index=True': It will search and filter till all bottom rows even if we find the data
    # With db_index=True': When Object finds it will just stop their
    username = models.CharField(max_length=35, unique = True)
    email = models.EmailField(max_length=35, unique = True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# we want user to login with email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # tell django how to manage these above type of objects
    objects = UserManager()

    def __str__(self):
        return self.email

