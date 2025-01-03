from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        
        role = extra_fields.get("role")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        if password:
            user.set_password(password)  # Hash the password
        else:
            raise ValueError("Password must be provided.")
        user.save(using=self._db)
        
         # Create role-specific instances
        if role == "guide":
            from core.models._Guide import Guide
            Guide.objects.create(user=user)  # Create Guide with default values
        elif role == "visitor":
            from core.models._Visitor import Visitor
            Visitor.objects.create(user=user, type="individual")  # Default type
        elif role == "advisor":
            from core.models._Advisor import Advisor
            Advisor.objects.create(user=user)
        elif role == "coordinator":
            from core.models._Advisor import Advisor
            Advisor.objects.create(user=user, isCoordinator=True, authorizedDay=[i for i in range(7)])

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('secretary', 'Secretary'),
        ('coordinator', 'Coordinator'),
        ('advisor', 'Advisor'),
        ('guide', 'Guide'),
        ('visitor', 'Visitor'),
    ]
    
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)  # Required for admin
    is_active = models.BooleanField(default=True)  # Required for admin
    profile_picture = models.URLField(
        max_length=255,
        blank=True,
        default="https://via.placeholder.com/150?text=No+Profile"
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'      # The field used as the unique identifier for the user