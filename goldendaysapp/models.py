from django.db import models
from uuid import uuid4
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
        
class Candidate(models.Model):
    candidate_id = models.CharField(max_length=50, unique=True, editable=False)
    candidate_name = models.CharField(max_length=200)
    phone= models.CharField(max_length=15)
    dob = models.DateField()
    registered_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.CASCADE,blank=True, null=True, related_name='registered_candidates')
    aadhar_number = models.CharField(max_length=20, unique=True)
    aadhar_file = models.FileField(upload_to='aadhar_files/', blank=True, null=True)
    pregancy_num= models.IntegerField()
    child_name = models.CharField(max_length=200, blank=True, null=True)
    lmp_date = models.DateField(blank=True, null=True)
    pan_no = models.CharField(max_length=20, unique=True)
    pan_file = models.FileField(upload_to='pan_files/', blank=True, null=True)
    account_number = models.CharField(max_length=30, unique=True)
    ifsc_code = models.CharField(max_length=20)
    verified_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.SET_NULL, related_name='verified_candidates', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    dob_child = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):

        if not self.candidate_id:

            self.candidate_id = (
                f"CAND-{uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)
        
class Intervention1(models.Model):
    candidate_id = models.ForeignKey(Candidate,to_field='candidate_id', on_delete=models.SET_NULL, blank=True, null=True,related_name='interventions1')
    intervention_opportunity = models.CharField(max_length=100)
    ques_answer=models.JSONField(blank=True, null=True)
    is_eligible = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    money_transferred_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.SET_NULL, related_name='created_interventions1', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Intervention2(models.Model):
    candidate_id = models.ForeignKey(Candidate,to_field='candidate_id', on_delete=models.SET_NULL,blank=True, null=True, related_name='interventions2')
    intervention_opportunity = models.CharField(max_length=100)
    ques_answer=models.JSONField(blank=True, null=True)
    is_eligible = models.BooleanField(default=False)
    money_transferred_status = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.SET_NULL, related_name='created_interventions2', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Intervention3(models.Model):
    candidate_id = models.ForeignKey(Candidate,to_field='candidate_id', on_delete=models.SET_NULL,blank=True, null=True, related_name='interventions3')
    intervention_opportunity = models.CharField(max_length=100)
    ques_answer=models.JSONField(blank=True, null=True)
    is_eligible = models.BooleanField(default=False)
    money_transferred_status = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.SET_NULL, related_name='created_interventions3', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Intervention4(models.Model):

    candidate_id = models.ForeignKey(Candidate,to_field='candidate_id', on_delete=models.SET_NULL, blank=True, null=True,related_name='interventions4')
    intervention_opportunity = models.CharField(max_length=100)
    ques_answer=models.JSONField(blank=True, null=True)
    is_eligible = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)
    money_transferred_status = models.BooleanField(default=False)
    created_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.SET_NULL, related_name='created_interventions4', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class QuestionnaireIntervention(models.Model):
    intervention = models.CharField(max_length=100)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    