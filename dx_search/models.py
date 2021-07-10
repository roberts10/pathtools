from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    SQL_username = models.CharField(max_length=128, unique=False)

    SQL_password = models.CharField(max_length=128, unique=False)

    # This now denotes an "analyst"
    analyst_status = models.BooleanField(default=False)

    last_password_change = models.DateTimeField("Last Password Change", default=datetime.datetime.now())

    def __str__(self):
        return self.user.username

class Case(models.Model):
    case_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.case_id

class Case_Set(models.Model):
    name = models.CharField(max_length = 30, unique = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cases =  models.ManyToManyField('Case')
    create_datetime = models.DateTimeField("Creation Timestamp", default=datetime.datetime.now())

    def __str__(self):
        return self.name

class Download_Request(models.Model):

    #User details
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=48)

    #secondary_user = models.ForeignKey(User, related_name = 'Primary_User', on_delete=models.CASCADE, null=True)

    requestor_last_name = models.CharField(max_length = 30, unique = False, blank = True)
    requestor_first_name = models.CharField(max_length = 30, unique = False, blank = True)
    requestor_email = models.CharField(max_length = 30, unique = False, blank = True)
    analyst_request  = models.BooleanField("Analyst Request", default=False)

    case_set = models.ForeignKey(Case_Set, related_name = 'Secondar_User', on_delete=models.CASCADE, null=True)

    # Status of request
    status_choices = [('New', 'New'), ('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Completed', 'Completed')]
    status = models.CharField("Request Status", max_length = 20, choices = status_choices, default = 'New')

    # Type of request
    type_choices = [('IRB', 'Research with IRB'), ('Case_Finding', 'Not Research (Case-Finding)')]
    request_type = models.CharField("Request Type", max_length = 20, choices = type_choices, default = 'IRB')

    # Datetime objects for request and execution time 
    request_datetime = models.DateTimeField("Request Timestamp", default=datetime.datetime.now())
    execute_datetime = models.DateTimeField("Execute Timestamp", null=True)
    execute_user = models.CharField("Executed By", max_length=256, unique=False, )
    
    #Case fields
    accession_number = models.BooleanField("Accession Number", default=False)
    staff = models.BooleanField("Assigned Staff", default=False)
    specimen_class = models.BooleanField("Copath Specimen Class", default=False)
    MRN = models.BooleanField("Patient MRN", default=False)
    DOB = models.BooleanField("Patient DOB", default=False)
    age = models.BooleanField("Patient Age", default=False)
    sex = models.BooleanField("Patient Sex", default=False)
    first_name = models.BooleanField("Patient First Name", default=False)
    last_name  = models.BooleanField("Patient Last Name", default=False)
    date = models.BooleanField("Accession Date", default=False)
    text = models.BooleanField("Final, Comment, Addendums", default=False)
    clinical = models.BooleanField("Clinical Information", default=False)
    gross = models.BooleanField("Gross Description", default=False)
    synoptic = models.BooleanField("Synoptic", default=False)
    intraoperative = models.BooleanField("Intraoperative Diagnosis", default=False)
    specimen_type = models.BooleanField("Specimen Type (sp, cyto, bone marrow)", default=False)

    # Extra stuff
    IRB_number = models.CharField(max_length=128, verbose_name='IRB_number (not required for non-research requests)', unique=False, null=True,  blank=True)
    collection_sheet = models.FileField(null=True, verbose_name = 'IRB approved data collection sheet (not required for non-research requests)',  blank=True)
    notes = models.TextField("Notes", default='')

