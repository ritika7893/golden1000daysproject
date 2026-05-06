from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
import random
from datetime import datetime
from django.utils import timezone
import re
import uuid
from django.db import IntegrityError

from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
def generate_id(prefix):
    current_year = datetime.now().year
    random_number = random.randint(100000, 999999)
    return f"{prefix}/{current_year}/{random_number}"
class AllLog(models.Model):
    id = models.AutoField(primary_key=True)
    unique_id = models.CharField(unique=True, max_length=50, editable=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15,blank=True, null=True)
    username = models.CharField(max_length=120, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255,default='')
    role = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False