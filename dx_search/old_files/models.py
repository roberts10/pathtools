from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    SQL_username = models.CharField(max_length=128, unique=False)

    SQL_password = models.CharField(max_length=128, unique=False)

    role = models.CharField(max_length=128, unique=False, default='regular')

    research_status = models.BooleanField(default=False)

    last_search = models.CharField(max_length=256, unique=False, default='')


    def __str__(self):
        return self.user.username

class Download_Options(models.Model):
    accession_number = models.BooleanField("Accession Number")
    date = models.BooleanField("Accession Date")
    staff = models.BooleanField("Assigned Staff")
    name = models.BooleanField("Patient Name")
    MRN = models.BooleanField("Patient MRN")
    DOB = models.BooleanField("Patient DOB")
    age = models.BooleanField("Patient Age")
    sex = models.BooleanField("Patient Sex")
    text = models.BooleanField("Diagnostic Text", default=None)
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()
#
