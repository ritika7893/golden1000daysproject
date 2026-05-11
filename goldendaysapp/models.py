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
    username = models.CharField(max_length=120,null=True, blank=True)
    password = models.CharField(max_length=255,default='')
    role = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'unique_id'
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
    dob = models.DateField(blank=True, null=True)
    registered_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.CASCADE,blank=True, null=True, related_name='registered_candidates')
    aadhar_number = models.CharField(max_length=20)
    aadhar_file = models.FileField(upload_to='aadhar_files/', blank=True, null=True)
   
    child_name = models.CharField(max_length=200, blank=True, null=True)
    lmp_date = models.DateField(blank=True, null=True)
    pan_no = models.CharField(max_length=20)
    pan_file = models.FileField(upload_to='pan_files/', blank=True, null=True)
    account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=20,blank=True, null=True)
    verified_by = models.ForeignKey(AllLog,to_field='unique_id', on_delete=models.SET_NULL, related_name='verified_candidates', blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    dob_child = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_candidate_id(self):

        current_year = datetime.now().year

        username = (
            self.registered_by.username.upper()
            if self.registered_by and self.registered_by.username
            else "USER"
        )

        prefix = f"CAN/{current_year}/{username}/"

        last_candidate = Candidate.objects.filter(
            candidate_id__startswith=prefix
        ).order_by('-candidate_id').first()

        if last_candidate:

            last_number = int(
                last_candidate.candidate_id.split("/")[-1]
            )

            next_number = last_number + 1

        else:

            next_number = 1

        return f"{prefix}{str(next_number).zfill(5)}"

    def save(self, *args, **kwargs):

        if not self.candidate_id:

            self.candidate_id = self.generate_candidate_id()

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


from django.db import models


# =========================
# Common Abstract Model
# =========================

class AWCBaseModel(models.Model):
    district_code = models.CharField(max_length=120)
    project = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    awc_code = models.CharField(max_length=100)
    awc = models.CharField(max_length=200)
    awc_hindi = models.CharField(max_length=500, blank=True, null=True)
    awc_type = models.CharField(max_length=100)
    code1 = models.CharField(max_length=100)
    code2 = models.CharField(max_length=100)
    edit_time = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True


# =========================
# District Tables
# =========================

class Almora(AWCBaseModel):
    class Meta:
        db_table = "almora"


class Bageshwar(AWCBaseModel):
    class Meta:
        db_table = "bageshwar"


class Chamoli(AWCBaseModel):
    class Meta:
        db_table = "chamoli"


class Champawat(AWCBaseModel):
    class Meta:
        db_table = "champawat"


class Dehradun(AWCBaseModel):
    class Meta:
        db_table = "dehradun"


class Haridwar(AWCBaseModel):
    class Meta:
        db_table = "haridwar"


class Nanital(AWCBaseModel):
    class Meta:
        db_table = "nanital"


class Pauri(AWCBaseModel):
    class Meta:
        db_table = "pauri"


class Pithoragarh(AWCBaseModel):
    class Meta:
        db_table = "pithoragarh"


class Rudraprayag(AWCBaseModel):
    class Meta:
        db_table = "rudraprayag"


class Tehri(AWCBaseModel):
    class Meta:
        db_table = "tehri"


class Usnagar(AWCBaseModel):
    class Meta:
        db_table = "usnagar"


class Uttarkashi(AWCBaseModel):
    class Meta:
        db_table = "uttarkashi"


# =========================
# District Login Table
# =========================

class District(models.Model):
    district = models.CharField(max_length=500)
    bill_use = models.CharField(max_length=200)
    sdname = models.CharField(max_length=500)
    db_use = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    def_pass = models.CharField(max_length=200, default="8266")
    stat_fin = models.CharField(max_length=200)

    class Meta:
        db_table = "district"

    def __str__(self):
        return self.district


# =========================
# CDPO Login Table
# =========================

class CdpoLogin(models.Model):
    district = models.CharField(max_length=100)
    bill_use = models.CharField(max_length=200)
    project_code = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    project_show = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    stat_fin = models.CharField(max_length=200)
    ang_pur = models.CharField(max_length=20)
    adhar_stat = models.CharField(
        max_length=200,
        default="unverified"
    )

    class Meta:
        db_table = "cdpo_login"

    def __str__(self):
        return self.project_name


# =========================
# Sector Login Table
# =========================

class SectorLogin(models.Model):

    sdname = models.CharField(max_length=200, blank=True, null=True)

    district = models.CharField(max_length=200, blank=True, null=True)

    project_code = models.CharField(max_length=200, blank=True, null=True)

    project_name = models.CharField(max_length=200, blank=True, null=True)

    sector = models.CharField(max_length=200, blank=True, null=True)

    sector_incharge = models.CharField(max_length=200, blank=True, null=True)

    incharge_mob = models.CharField(max_length=200, blank=True, null=True)

    password = models.CharField(max_length=100, blank=True, null=True)

    def_pass = models.CharField(max_length=20, blank=True, null=True)

    updated_on = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "sector_login"

    def __str__(self):
        return f"{self.sector} - {self.project_name}"