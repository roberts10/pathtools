from .models import Profile
from .models import Download_Request, Case_Set
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext, gettext_lazy as _
import datetime
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)
import arrow

from django.core.exceptions import ValidationError

# This class is to enable lock-out code
class InvalidLoginAttemptsCache(object):
    @staticmethod
    def key(username):
        key = 'invalid_login_attempt_{}'.format(username)
        logger.debug('Generated key: %s', key)
        return key

    @staticmethod
    def value(lockout_timestamp, timebucket):
        return {
            'lockout_start': lockout_timestamp,
            'invalid_attempt_timestamps': timebucket
            }

    @staticmethod
    def delete(username):
        try:
            cache.delete(InvalidLoginAttemptsCache.key(username))
        except Exception as e:
            logger.exeption(e)

    @staticmethod
    def set(username, timebucket, lockout_timestamp=None):
        try:
            key = InvalidLoginAttemptsCache.key(username)
            value = InvalidLoginAttemptsCache.value(lockout_timestamp, timebucket)
            cache.set(key, value)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def get(username):
        try:
            key = InvalidLoginAttemptsCache.key(username)
            return cache.get(key)
        except Exception as e:
            logger.exception(e)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('SQL_username', 'SQL_password')

# class OptionsForm(forms.ModelForm):
#     class Meta:
#         model = Download_Options
#         fields = ('accession_number', 'MRN', 'DOB', 'age', 'sex', 'first_name', 'last_name', 'date', 'staff', 'text', 'IRB_number')
#

class DownloadForm(forms.ModelForm):

    class Meta:
        model = Download_Request
        exclude = ('user', 'query', 'notes', 'execute_datetime', 'request_datetime', 'execute_user', 'status', 'case_set', 'requestor_last_name', 'requestor_first_name', 'requestor_email', 'analyst_request')

    field_order = [ 'accession_number', 'date', 'MRN', 'DOB', 'age', 'sex', 'last_name', 'first_name', 'gross', 'clinical', 'text', 'synoptic', 'intraoperative', 'staff', 'specimen_type','specimen_class', 'IRB_number', 'collection_sheet'] 

class DownloadFormAnalyst(forms.ModelForm):

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if cleaned_data.get('request_type') == 'IRB':
    #         raise form.ValidationError({'IRB_number':'Validation ERROR'})

    class Meta:
        model = Download_Request
        exclude = ('user', 'query', 'notes', 'execute_datetime', 'request_datetime', 'execute_user', 'status', 'case_set', 'analyst_request')

    field_order = [ 'requestor_last_name', 'requestor_first_name', 'requestor_email', 'accession_number', 'date', 'MRN', 'DOB', 'age', 'sex', 'last_name', 'first_name', 'gross', 'clinical', 'text', 'synoptic', 'intraoperative', 'staff', 'specimen_type','specimen_class', 'IRB_number', 'collection_sheet'] 

class AddNoteForm(forms.Form):
    note = forms.CharField(label = 'Add Note', max_length =500)

# This is the form that ANALYSTS use for case-finding activities
# class CaseFindingForm(forms.ModelForm):
#
#     class Meta:
#         model = Download_Request
#         exclude = ('username', 'query', 'datetime', 'notes', 'execute_datetime', 'request_datetime', 'execute_user', 'IRB_number', 'collection_sheet', 'request_type' , 'status')
#
#     field_order = ['user_email', 'user_last_name', 'user_first_name', 'staff', 'accession_number', 'date', 'MRN', 'DOB', 'age', 'sex', 'name', 'gross', 'clinical', 'text', 'synoptic', 'intraoperative',] 


class Case_Search_Submission_Form(forms.Form):

    name = forms.CharField(label = 'Name for list of cases',max_length = 40)
    input_choices = [('accession_numbers', 'Accession Numbers'),('MRN', 'MRN'), ('name_dob', 'Name and DOB')]
    input_type = forms.ChoiceField( choices = input_choices)
    text = forms.CharField(label = 'Input', widget=forms.Textarea)

class Name_Entry_Form(forms.Form):

    name = forms.CharField(label = 'Name for list of cases',max_length = 40)

# Subclass AuthenicationForm to introduce lockout logic
class CustomAuthenticationForm(AuthenticationForm):

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive. TEST"
        ),
        'inactive': _("This account is inactive."),
        'locked_out': _(
            "Your account has been locked out due to multiple failed attempts. Your lock-out will be lifted after 30 min."
            ),
    }

    def clean(self):
        now = datetime.datetime.now() 
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        logger.debug('Form username is : %s', username)

        #Preauthentication code to determine if user is locked out
        cache_results = InvalidLoginAttemptsCache.get(username)

        logger.debug("Cache contents: %s", cache_results)

        if cache_results and cache_results.get('lockout_start'):

            lockout_start = arrow.get(cache_results.get('lockout_start'))
            locked_out = lockout_start >= arrow.utcnow().shift(minutes=-30)
            if not locked_out:
                logger.debug('%s lock out has expired', username)
                InvalidLoginAttemptsCache.delete(username) 
            else:
                # User is locked out, raise error
                logger.debug('%s is locked out.  Raise exception', username)
                raise self.get_locked_out_error()
        else:
            # NOT locked out, proceed with request
            logger.debug('%s is not locked out', username)
            pass

        # Stock code, execute when user is not locked out
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            # Run this when the authentication fails
            # Start the lock-out process
            if self.user_cache is None:
                logger.debug('%s failed to authenticate', username)
                cache_results = InvalidLoginAttemptsCache.get(username) 
                invalid_attempt_timestamps = cache_results['invalid_attempt_timestamps'] if cache_results else []
                logger.debug('Initial Cache invalid_attempt_timestamps: %s', invalid_attempt_timestamps)
                initial_lockout_timestamp = cache_results['lockout_start'] if cache_results else ''
                logger.debug('Initial lockout timestamp: %s', initial_lockout_timestamp)

                lockout_timestamp = None
                now = arrow.utcnow()
                # Clear any invalid attempts that were longer ago than the range
                invalid_attempt_timestamps = [timestamp for timestamp in invalid_attempt_timestamps if timestamp > now.shift(minutes=-30).timestamp]
                # Add the current timestamp to the list
                invalid_attempt_timestamps.append(now.timestamp)
                #check to see if user has enough invalid login attempts to lock out

                logger.debug('Number of timestamps: %s', len(invalid_attempt_timestamps))
                if len(invalid_attempt_timestamps) >= 10:
                    lockout_timestamp = now.timestamp
                    InvalidLoginAttemptsCache.set(username, invalid_attempt_timestamps, lockout_timestamp)
                    raise self.get_locked_out_error()

                else:
                    InvalidLoginAttemptsCache.set(username, invalid_attempt_timestamps, lockout_timestamp)
                    raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

    def get_locked_out_error(self):
        return forms.ValidationError(
            self.error_messages['locked_out'],
            code='locked_out',
            #params={'username':self.username_field.verbose_name},
            )

        
