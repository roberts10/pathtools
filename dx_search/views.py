from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache
from django.template.loader import get_template
from django.template  import Context
import pyodbc
import sys
import re
import os
from django import forms
from .models import Profile, Download_Request, Case, Case_Set 
from .forms import ProfileForm, DownloadForm, AddNoteForm, Case_Search_Submission_Form, Name_Entry_Form, DownloadFormAnalyst, CustomAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
import datetime
import pandas as pd
from dateutil.parser import parse
from django.contrib.auth import logout

# Set SQL database parameters
DRIVER = 'ODBC Driver 17 for SQL Server'

DATABASE = 'Pathtools'
# New Production server (as of 4/2/2020)

SERVER = os.environ.get("SERVER")

server = 'pathtools.ccf.org'

import logging
logger = logging.getLogger(__name__)

############################################################

###  Django Auth Subclassed Functions             ######

###########################################################

# Check if password is expired
class CustomLoginView(LoginView):

    form_class = CustomAuthenticationForm

    def get_success_url(self):

        user = self.request.user

        last_change = user.profile.last_password_change
        
        delta = datetime.datetime.now() - last_change

        if delta.days > 90:
            logger.debug('password change greater than 90')
            #logout(self.request)
            return resolve_url(settings.EXPIRED_REDIRECT_URL)

        else:

            logger.debug('password change less than 90')
            return resolve_url(settings.LOGIN_REDIRECT_URL)

#Update Profile with password change timestamp
class CustomPasswordChangeView(PasswordChangeView):

    #success_url = reverse_lazy('auth_password_change_done')

    def form_valid(self, form):

        profile = Profile.objects.get(user=form.user)
        profile.last_password_change = datetime.datetime.now() 
        profile.save()
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class CustomPasswordChangeDoneView(PasswordChangeDoneView):

    template_name = 'registration/password_change_done.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
############################################################

###  SQL CORE DATABASE FUNCTIONS                          ######

###########################################################


# Helper function to get SQL credentials from user's profile
def get_SQL_credentials(request):
    
    SQL_username =  request.user.profile.SQL_username
    
    SQL_password = request.user.profile.SQL_password

    return {'username':SQL_username, 'password':SQL_password}

def get_SQL_cursor(request):

    response = get_SQL_credentials(request)

    UID = response['username']
    PWD = response['password']

    connection_string = ('DRIVER=%s;SERVER=%s;UID=%s;PWD=%s;DATABASE=%s' % (DRIVER,SERVER,UID,PWD,DATABASE))

    ##establish connection
    cxn = pyodbc.connect(connection_string)

    cursor = cxn.cursor()

    return cursor

############################################################

###  HELPER FUNCTIONS                                ######

###########################################################

def email_analysts():

    subject, from_email = 'New Search Request', 'admin@pathtools.org' 
    text_content = """Dear analysts, A new search request has been submitted in Pathtools. Have a nice day, Pathtools Admin"""
    html_content = """Dear analysts, </br> </br> A new search request has been submitted in Pathtools. <p> <p> Have a nice day, </p> <p> Pathtools Admin</p>"""
    msg =  EmailMultiAlternatives(subject, text_content, from_email, ['roberts10@ccf.org', 'COPATHCA@CCF.ORG'])
    #msg =  EmailMultiAlternatives(subject, text_content, from_email, ['roberts10@ccf.org',])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Helper function that converts MySQL syntax to T SQL syntax
def format_helper(string):
    #Compile regex 
    #regex = re.compile(r'(\w+?)\s(CONTAINS[()])')
    regex = re.compile(r'(\w+?)\s(N?O?T?\s?CONTAINS[()])')
    string = regex.sub('\g<2>\g<1>, ', string)
    string = re.sub("""(?<=[a-zA-Z])\\\\\'""", """\'\'""", string)
    return string

# Helper function that parses out the diagnostic terms from the SQL query string
def ParseTerms(query):
    query = re.sub('\'\'', '\'', query)
    regex = re.compile('"(.+?)"')
    match = regex.findall(query)
    regex_list = [re.compile(i, re.I) for i in match]
    return(regex_list)

def AddNote(request, query, note):
    now = datetime.datetime.now()
    datetime_string = now.strftime("%m/%d/%Y, %H:%M")
    query.notes = query.notes + datetime_string + ':' + '\t' + request.user.username + ':' + '\t' + note + '\n\n'
    query.save()

#This function takes a long string containing cases sep by newlines.
#It parses the cases
#Returns a  SET of cases
def case_MRN_parser(input):

    list = {x for x in map(lambda x: x.upper().strip(), input.split())}

    return list

# RETURNS A SET OF STRINGS 
def case_DOB_name_parser(input):
    
    list = input.upper().split('\n')

    csv_set = set()
    for line in list:

        last, first, DOB = line.split('\t')
        timestamp = parse(DOB, fuzzy=True)
        formatted_string = timestamp.strftime('%Y-%m-%d')
        csv_string = last.strip() + ',' + first.strip()[0] + ',' + formatted_string
        csv_set.add(csv_string)

    return csv_set

def reject_request(request, query_id):

    query = Download_Request.objects.get(id=query_id)

    query.status = 'Rejected'
    query.execute_user = request.user.username
    query.execute_datetime = datetime.datetime.now()
    query.save()
    AddNote(request, query, 'REJECTED')

    redirect_string = 'download_request_instance_manager/' + str(query_id)

    return redirect(redirect_string)

def pending_request(request, query_id):

    query = Download_Request.objects.get(id=query_id) 
    query.status = 'Pending'
    query.execute_user = request.user.username
    query.execute_datetime = datetime.datetime.now()
    query.save()
    AddNote(request, query, 'MADE PENDING')

    redirect_string = 'download_request_instance_manager/' + str(query_id)

    return redirect(redirect_string)

# View to tell the user that their request has been submitted
def request_submitted(request):

    profile = Profile.objects.get(user=request.user)

    if profile.analyst_status:
        return redirect('analyst_dashboard')

    else:
        email_analysts()
        return render(request, 'dx_search/request_submitted.html')

def load_case_set_to_memory(request, case_set_id):

    request.session['loaded_case_set_id'] = case_set_id

    return redirect('dx_download')

def clear_loaded_case_set(request):

    request.session['loaded_case_set_id'] =  False

    return redirect('dx_download')

def delete_case_set(request, case_set_id):

    case_set = Case_Set.objects.get(id=case_set_id)

    case_set.delete()

    return redirect('case_upload_portal')

def delete_case_set_goto_dashboard(request, case_set_id):

    case_set = Case_Set.objects.get(id=case_set_id)

    case_set.delete()

    return redirect('case_set_dashboard')
    

# Takes a list of case data extracted from Pathtools 
# The case_result_list variable is a list of dictionaries, each case is one dictionary
# Return a pandas dataframe
def dataframe_writer(case_result_list):
    columns = ['case_id', 'age', 'sex', 'DOB', 'MRN', 'staff', 'specimen_class', 'accession_date', 'text', 'first_name', 'last_name', 'gross', 'clinical', 'synoptic', 'intraoperative', 'specimen_type']
    df = pd.DataFrame(columns = columns)

    for result in case_result_list:
        df = df.append(result, ignore_index = True)
        
    return df

def PHI_filter(df, download_request):

    option_list =  [
            ['case_id', download_request.accession_number],
            ['age', download_request.age],
            ['sex', download_request.sex],
            ['DOB', download_request.DOB],
            ['MRN', download_request.MRN],
            ['staff', download_request.staff],
            ['specimen_class', download_request.specimen_class],
            ['accession_date', download_request.date],
            ['text', download_request.text],
            ['first_name', download_request.first_name],
            ['last_name', download_request.last_name],
            ['gross', download_request.gross],
            ['clinical', download_request.clinical],
            ['synoptic', download_request.synoptic],
            ['intraoperative', download_request.intraoperative],
            ['specimen_type', download_request.specimen_type],
            ]

    true_fields = [field[0] for field in option_list if field[1]]

    cols = []
    for true_field in true_fields:
        
        for column in df.columns:
            if column.startswith(true_field):
                cols.append(column)
    
    df_out = df[cols]
    
    return df_out

def patient_case_id_history_search(request, case_set_id):

    case_set_input = Case_Set.objects.get(id=case_set_id)

    if request.method == 'POST':

        form = Name_Entry_Form(request.POST)

        if form.is_valid():

            case_set = Case_Set(user = request.user, name=form.cleaned_data['name'])
            case_set.save()

            query_set = case_set_input.cases.all()
            case_id_list = [case.case_id for case in query_set]

            results_list = execute_patient_case_id_history_search(request, case_id_list)

            for result in results_list: 
                case = Case.objects.get_or_create(case_id=result)
                case_set.cases.add(case[0])

            case_set.save()

            context_dictionary = {'case_set':case_set}

            return render(request, 'dx_search/case_upload_results.html', context_dictionary)

        else:
            HttpResponse('else option')

    else:

        name_entry_form = Name_Entry_Form()

        return render(request, 'dx_search/patient_case_id_history_search.html', {'name_entry_form':name_entry_form, 'history_search':True, 'case_set_input':case_set_input})

############################################################

###  MAJOR PAGE VIEWS                                ######

###########################################################
# View for 'About' page. Gets data using get_metadata help function

@login_required
def about(request):

    year_metadata, staff_metadata = get_metadata(request)

    counter = 0
    for i in year_metadata:
        counter += int(i[1])

    context_dict = {'variable':__name__, 'year_metadata':year_metadata, 'total':counter, 'staff_metadata':staff_metadata }

    return render(request, 'dx_search/about.html', context=context_dict)

# View for 'dx_search' page
#@login_required(login_url = server + '/accounts/login/')
@login_required(login_url = server + '/dx_search/login/')
#@login_required(login_url = server + '/login/')
def dx_search(request):
    context_dict = {'user': request.user}
    return render(request, 'dx_search/VA.html', context_dict)

# View for 'dx_download' page
#@login_required(login_url = server + '/accounts/login/')
@login_required(login_url = server + '/dx_search/login/')
#@login_required(login_url = server + '/login/')
def dx_download(request):

    try:
        loaded_case_set_id = request.session['loaded_case_set_id']
        loaded_case_set = Case_Set.objects.get(id=loaded_case_set_id)
    except:
        loaded_case_set = False

    context_dict = {'user': request.user, 'loaded_case_set':loaded_case_set}
    return render(request, 'dx_search/VA_download.html', context_dict)

# View for the 'analyst_view' page
@login_required(login_url = server + '/accounts/login/')
def analyst_dashboard(request):

    new_queries = Download_Request.objects.filter(status='New')
    pending_queries = Download_Request.objects.filter(status='Pending')
    completed_queries = Download_Request.objects.filter(status='Completed')
    rejected_queries = Download_Request.objects.filter(status='Rejected')
    
    return render(request, 'dx_search/analyst_dashboard.html', {'new_queries': new_queries, 'pending_queries': pending_queries, 'completed_queries': completed_queries, 'rejected_queries':rejected_queries})

# View given to the analyst when they are evaluated a search request 
@login_required(login_url = server + '/accounts/login/')
def download_request_instance_manager(request, query_id):
    query = Download_Request.objects.get(id=query_id) 

    case_set = query.case_set.cases.all()

    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']
            AddNote(request, query, note)
    else:
        form = AddNoteForm()

    return render(request, 'dx_search/download_request_instance_manager.html', {'query':query, 'form':form, 'case_set': case_set})

# This view is displayed to the user when a search request is initiated
@login_required(login_url = server + '/accounts/login/')
def download_request(request, case_set_id):

    profile = Profile.objects.get(user=request.user)

    case_set = Case_Set.objects.get(id=case_set_id)

    if request.method == 'POST' and profile.analyst_status:

        download_form = DownloadFormAnalyst(request.POST, request.FILES)

        if download_form.is_valid():

            model = download_form.save(commit=False)

            model.analyst_request = True
                
            model.user = request.user
            model.case_set = case_set

            model.save()

            return redirect('request_submitted') 

    elif request.method == 'POST' and not profile.analyst_status:

        download_form = DownloadForm(request.POST, request.FILES) 
            
        if download_form.is_valid():

            model = download_form.save(commit=False)

            model.user = request.user
            model.case_set = case_set

            model.save()

            return redirect('request_submitted') 

    #elif request.method == 'GET' and 'AND accession_date' in request.session['SQL_query']:
    elif request.method == 'GET' and case_set.cases.count() < 5001:


        if profile.analyst_status:

            download_form = DownloadFormAnalyst()

        else:

            download_form = DownloadForm()

        return render(request, 'dx_search/download_request.html', {'download_form':download_form, 'case_set':case_set})

    else:
        return HttpResponse('<h3> ERROR: Download requests limited to 5000 cases. </h3>')

# This is a function for analysts to change the search options
@login_required(login_url = server + '/accounts/login/')
@csrf_exempt
def change_options(request, query_id):

    query = Download_Request.objects.get(id=query_id) 

    if request.method == 'GET':
        download_form = DownloadFormAnalyst(instance=query)  
        
        return render(request, 'dx_search/change_options.html', {'query':query, 'options_form':download_form}) 

    elif request.method == 'POST':

        download_form = DownloadFormAnalyst(request.POST, request.FILES, instance = query) 

        if download_form.is_valid():

            # model = download_form.save(commit=False)
            # model.user_first = request.user.first_name
            # model.user_last = request.user.last_name
            # model.username = request.user.username  
            # model.email = request.user.email
            # model.query = request.user.profile.last_search
            download_form.save()

        else:
            return HttpResponse('NOT VALID')

        new_queries = Download_Request.objects.filter(status='New')
        pending_queries = Download_Request.objects.filter(status='Pending')
        completed_queries = Download_Request.objects.filter(status='Completed')
        rejected_queries = Download_Request.objects.filter(status='Rejected')
    
        #return render(request, 'dx_search/analyst_dashboard.html', {'new_queries': new_queries, 'pending_queries': pending_queries, 'completed_queries': completed_queries, 'rejected_queries':rejected_queries})
        return redirect('download_request_instance_manager/' + str(query.id))

    else:
        return HttpResponse('ERROR, NOT POST OR GET')

# New view for showing case_id/MRN/patient upload form
# Shows case_manager underneath
@login_required(login_url = server + '/accounts/login/')
def case_upload_portal(request):

    if request.method == 'POST':
        
        #form = Case_Search_Submission_Form(request.POST, request.FILES)
        form = Case_Search_Submission_Form(request.POST)

        if form.is_valid():

            if form.cleaned_data['input_type'] == 'accession_numbers':

                text = form.cleaned_data['text']

                input_python_set = case_MRN_parser(text)

                # This search is to verify cases are in the DB
                results_list = execute_case_id_search_by_case_list(request, input_python_set)
                case_set = Case_Set(user = request.user, name=form.cleaned_data['name'])
                case_set.save()


                output_python_set = set()
                for result in results_list:
                    output_python_set.add(result)
                    case = Case.objects.get_or_create(case_id=result)
                    case_set.cases.add(case[0])

                case_set.save()

                set_difference = input_python_set - output_python_set

                context_dictionary = {'case_set':case_set, 'set_difference':set_difference, 'set_size':len(set_difference)}

                return render(request, 'dx_search/case_upload_results.html', context_dictionary)
            
            elif form.cleaned_data['input_type'] == 'MRN':

                text = form.cleaned_data['text']

                input_MRN_set = case_MRN_parser(text)

                # This search is to verify cases are in the DB
                results_list = execute_case_id_search_by_MRN_list(request, input_MRN_set)

                # Instantiate Case_set
                case_set = Case_Set(user = request.user, name=form.cleaned_data['name'])
                case_set.save()

                # Loop to populate Case Set instance 
                output_MRN_set = set()
                for result in results_list:
                    output_MRN_set.add(result[1])
                    case = Case.objects.get_or_create(case_id=result[0])
                    case_set.cases.add(case[0])

                case_set.save()

                set_difference =  input_MRN_set - output_MRN_set

                context_dictionary = {'case_set':case_set, 'set_difference':set_difference, 'output_patient_size':len(output_MRN_set),'difference_size':len(set_difference)}

                return render(request, 'dx_search/case_upload_results.html', context_dictionary)
            
            else:

                text = form.cleaned_data['text']

                input_name_DOB_set = case_DOB_name_parser(text)

                # # This search is to verify cases are in the DB
                # Function returns a list of lists
                results_list = execute_case_id_search_by_name_DOB(request, input_name_DOB_set)
                
                # Instantiate Case_set
                case_set = Case_Set(user = request.user, name=form.cleaned_data['name'])
                case_set.save()

                # Loop to populate Case Set instance 
                output_name_DOB_set = set()
                for result in results_list:
                    output_name_DOB_set.add(result[1] + ',' + result[2] + ',' + str(result[3]))
                    case = Case.objects.get_or_create(case_id=result[0])
                    case_set.cases.add(case[0])

                case_set.save()

                set_difference = input_name_DOB_set - output_name_DOB_set

                context_dictionary = {'case_set':case_set, 'set_difference':set_difference, 'output_patient_size':len(output_name_DOB_set), 'difference_size':len(set_difference)}

                return render(request, 'dx_search/case_upload_results.html', context_dictionary)
                # context_dictionary = {'output':output_name_DOB_set, 'input':input_name_DOB_set, 'difference':set_difference}
                #
                # return render(request, 'dx_search/tester.html', context_dictionary)


    elif request.method == 'GET':

        submission_form = Case_Search_Submission_Form()

        return render(request, 'dx_search/case_upload_portal.html', {'submission_form':submission_form })

    else:
        #
        return render(request, 'dx_search/case_upload_portal.html')

@login_required(login_url = server + '/accounts/login/')
def case_set_dashboard(request):

    try:
        loaded_case_set_id = request.session['loaded_case_set_id']
        loaded_case_set = Case_Set.objects.get(id=loaded_case_set_id)
    except:
        loaded_case_set = False

    user_case_set = Case_Set.objects.filter(user = request.user).order_by('-create_datetime')

    return render(request, 'dx_search/case_set_dashboard.html', {'user_case_set':user_case_set, 'loaded_case_set':loaded_case_set})

@login_required(login_url = server + '/accounts/login/')
def case_set_instance_manager(request, case_set_id):

    case_set = Case_Set.objects.get(id=case_set_id)

    return render(request, 'dx_search/case_set_instance_manager.html', {'case_set':case_set}) 

@login_required(login_url = server + '/accounts/login/')
def capture_cases(request):

    if request.method == 'POST':

        form = Name_Entry_Form(request.POST)

        if form.is_valid():

            SQL_filter_substring = request.session['SQL_string']

            cursor = get_SQL_cursor(request)

            try:
                case_set_id = request.session['loaded_case_set_id']
            except:
                case_set_id = False

            if case_set_id:
               case_set_instance = Case_Set.objects.get(id=case_set_id)
               case_query_set = case_set_instance.cases.all()

               cursor.execute('CREATE TABLE #TEMP (temp_case_id nchar(20))')

               join_substring = 'FROM [#TEMP] JOIN dbo.ap_case on [#TEMP].temp_case_id = case_id WHERE '

               for case_id in case_query_set:
                   query = "INSERT INTO #TEMP (temp_case_id) VALUES ('%s')" % (case_id)
                   cursor.execute(query)

            else:
                join_substring = 'FROM dbo.ap_case WHERE '

            final_query_string = 'SELECT TOP(5000) case_id '+ join_substring + SQL_filter_substring

            cursor.execute(final_query_string) 

            results = cursor.fetchall()
            
            case_set = Case_Set(user = request.user, name=form.cleaned_data['name'], create_datetime = datetime.datetime.now())

            case_set.save()
           
            for result in results:
                case = Case.objects.get_or_create(case_id=result[0])
                case_set.cases.add(case[0])

            case_set.save()

            return render(request, 'dx_search/capture_cases.html', {'case_set':case_set})

        else:
            return HttpResponse('FORM NOT VALID')
    else:
        
        if not 'accession_date' in request.session['SQL_string']:

            return HttpResponse("""<h3> An accession date range is required to capture cases for research purposes. </br> </br>
                    For IRB-approved research, this must conform to your IRB protocol. </br> </br>
                    Please hit the back button and try again. </h3>""")

        else:

            name_entry_form = Name_Entry_Form()

            return render(request, 'dx_search/capture_cases.html', {'name_entry_form':name_entry_form})

############################################################

###  SQL COMMAND FUNCTIONS                           ######

###########################################################

# THis is a function designed to find cases in the DB from the user upload portal
def execute_case_id_search_by_case_list(request, case_list):

    cursor = get_SQL_cursor(request)
    cursor.execute('CREATE TABLE #TEMP (temp_case_id nchar(20))')

    for case in case_list:

        query = "INSERT INTO #TEMP (temp_case_id) VALUES ('%s')" % (case)
        cursor.execute(query)
    
    select_substring = 'SELECT case_id '
    join_substring = 'FROM [#TEMP] JOIN dbo.ap_case on [#TEMP].temp_case_id = case_id'

    cursor.execute(select_substring + join_substring)

    results = cursor.fetchall()

    results_return = [result[0].rstrip() for result in results]

    return results_return
# THis is a function designed to find cases in the DB from the user upload portal
def execute_case_id_search_by_MRN_list(request, MRN_list):

    cursor = get_SQL_cursor(request)
    cursor.execute('CREATE TABLE #TEMP (temp_MRN nchar(30))')

    for MRN in MRN_list:

        query = "INSERT INTO #TEMP (temp_MRN) VALUES ('%s')" % (MRN)
        cursor.execute(query)
    
    select_substring = 'SELECT case_id, MRN '
    join_substring = 'FROM [#TEMP] JOIN dbo.ap_case on [#TEMP].temp_MRN = MRN'

    cursor.execute(select_substring + join_substring)

    results = cursor.fetchall()
    
    results_return_list = []
    for result in results:

        results_return_list.append([result[0].rstrip(), result[1].rstrip()])
        
    return results_return_list

# THis is a function designed to find cases in the DB from the user upload portal
# Returns a list (results_return_list) of lists [case_id, last_name, first_name, DOB]
def execute_case_id_search_by_name_DOB(request, record_list):

    cursor = get_SQL_cursor(request)
    cursor.execute('CREATE TABLE #TEMP (temp_last_name nchar(100), temp_first_name nchar(100), temp_DOB date)')

    for (last,first,DOB) in map(lambda list: list.split(','), record_list):


        query = "INSERT INTO #TEMP (temp_last_name, temp_first_name, temp_DOB ) VALUES ('%s', '%s', '%s')" % (last, first, DOB)

        cursor.execute(query)
    
    select_substring = 'SELECT case_id, last_name, first_name, DOB '
    join_substring = 'FROM [#TEMP] JOIN dbo.ap_case on [#TEMP].temp_DOB = DOB AND [#TEMP].temp_last_name = last_name AND LEFT([#TEMP].temp_first_name, 1) = LEFT(first_name ,1)'

    cursor.execute(select_substring + join_substring)

    results = cursor.fetchall()
    
    results_return_list = []
    for result in results:

        results_return_list.append([result[0].rstrip(), result[1].rstrip(), result[2][0].rstrip(), result[3]])
        
    return results_return_list

# THis is a function designed to find cases in the DB from the user upload portal
def execute_patient_case_id_history_search(request, case_list):

    cursor = get_SQL_cursor(request)
    cursor.execute('CREATE TABLE #TEMP (temp_case_id nchar(20))')

    for case in case_list:

        query = "INSERT INTO #TEMP (temp_case_id) VALUES ('%s')" % (case)
        cursor.execute(query)
    
    query = """SELECT B.case_id FROM 
    #TEMP JOIN dbo.ap_case as A on #TEMP.temp_case_id = A.case_id
    JOIN dbo.ap_case as B on A.last_name = B.last_name AND LEFT(A.first_name, 1) = LEFT(B.first_name,1) AND A.DOB = B.DOB"""

    cursor.execute(query)

    results = cursor.fetchall()

    results_return = [result[0].rstrip() for result in results]

    return results_return

# Purpose: Contains most of the logic for the preview search
# Input: SQL_query string passed in through POST dictionary
# Output: AJAX through results_test.html template 
# Only requests PHI-light fields from DB
@csrf_exempt
def execute_search_preview(request):

    start_timestamp = datetime.datetime.now()

    string = request.POST['key2']

    logger.debug("Raw String: %s ", string)

    cursor = get_SQL_cursor(request)
    formatted_string = "SELECT TOP(100) case_id, age, sex, staff, text from dbo.ap_case WHERE " + format_helper(string) 

    logger.debug("Helper Formatted: %s", formatted_string)

    cursor.execute(formatted_string) 
    results = cursor.fetchall()
    logger.debug("Number of Results: %s", len(results))

    ######################

    regex_list = ParseTerms(formatted_string)

    logger.debug("Regex List: %s", regex_list)
    output_results_list = []
    for i in results:

        dict = {'case_id': i[0], 'age': i[1], 'sex': i[2], 'staff': i[3], 'text': i[4]}

        for regex in regex_list:

            logger.debug("Regex in Regex List: %s", regex)
            dict['text'] = regex.sub(r'<mark>%s</mark>' % regex.pattern, dict['text'])  

        output_results_list.append(dict)

    context_dict = {'records':output_results_list, 'number':len(results)}

    ###################################################

    # try:
    #
    #     regex_list = ParseTerms(formatted_string)
    #     logger.debug("Regex List: %s", regex_list)
    #
    #     output_results_list = []
    #     for i in results:
    #
    #         for regex in regex_list:
    #             logger.debug("Regex in Regex List: %s", regex)
    #             marked_text = i[4]
    #             marked_text = regex.sub(r'<mark>%s</mark>' % regex.pattern, marked_text)
    #
    #
    #         record = [i[0], i[1], i[2], i[3], marked_text,] 
    #         output_results_list.append(record)
    #
    #     context_dict = {'records':output_results_list, 'number':len(output_results_list)}
    #
    # except:
    #     logger.debug("TERMS EXCEPT BLOCK")
    #     context_dict = {'records':results, 'number':len(results)}
    #
    #
    #LOGGING STUFF
    complete_timestamp = datetime.datetime.now()
    elapsed = complete_timestamp - start_timestamp
    log_string = request.user.username + '\t' + complete_timestamp.strftime("%x") + '\t' + complete_timestamp.strftime("%X") + '\t' +  string + '\t' + str(elapsed.total_seconds())
    logger.info(log_string)

    return render(request, 'dx_search/ajax_results_return_preview.html', context_dict)

@csrf_exempt
def execute_search_research(request):

    start_timestamp = datetime.datetime.now()

    string = request.POST['key2']
    cursor = get_SQL_cursor(request)
    select_substring = 'SELECT TOP(100) case_id, age, sex, staff, accession_date, text, clinical, synoptic, intraoperative, gross '
    #select_substring = 'SELECT  case_id, age, sex, staff, accession_date, text, clinical, synoptic, intraoperative, gross '
    count_select_substring = 'SELECT COUNT(*) '

    try:
        case_set_id = request.session['loaded_case_set_id']
    except:
        case_set_id = False

    if case_set_id:
       case_set_instance = Case_Set.objects.get(id=case_set_id)
       case_query_set = case_set_instance.cases.all()

       cursor.execute('CREATE TABLE #TEMP (temp_case_id nchar(20))')

       join_substring = 'FROM [#TEMP] JOIN dbo.ap_case on [#TEMP].temp_case_id = case_id WHERE '

       for case_id in case_query_set:
           query = "INSERT INTO #TEMP (temp_case_id) VALUES ('%s')" % (case_id)
           cursor.execute(query)

    else:
        join_substring = 'FROM dbo.ap_case WHERE '

    filter_substring = format_helper(string)
    final_query_string = select_substring + join_substring + filter_substring + " ORDER BY accession_date DESC"
    count_query_string = count_select_substring + join_substring + filter_substring

    cursor.execute(count_query_string)
    total_count = cursor.fetchone()[0]

    request.session['SQL_string'] =  filter_substring
    #
    cursor.execute(final_query_string) 

    results = cursor.fetchall()

    regex_list = ParseTerms(final_query_string)

    output_results_list = []
    for i in results:

        dict = {'case_id': i[0], 'age': i[1], 'sex': i[2], 'staff': i[3], 'accession_date': i[4], 'text': i[5], 'clinical': i[6], 'synoptic': i[7], 'intraoperative': i[8], 'gross':i[9]}

        for regex in regex_list:
            dict['text'] = regex.sub(r'<mark>%s</mark>' % regex.pattern, dict['text'])  
            try:
                dict['clinical'] = regex.sub(r'<mark>%s</mark>' % regex.pattern, dict['clinical'])
            except:
                pass
            try:
                dict['synoptic'] = regex.sub(r'<mark>%s</mark>' % regex.pattern, dict['synoptic'])
            except:
                pass
            try:
                dict['intraoperative'] = regex.sub(r'<mark>%s</mark>' % regex.pattern, dict['intraoperative'])
            except:
                pass

            output_results_list.append(dict)

    context_dict = {'records':output_results_list, 'number':total_count}

    complete_timestamp = datetime.datetime.now()
    elapsed = complete_timestamp - start_timestamp
    log_string = request.user.username + '\t' + complete_timestamp.strftime("%x") + '\t' + complete_timestamp.strftime("%X") + '\t' +  string + '\t' + str(elapsed.total_seconds())
    logger.info(log_string)


    return render(request, 'dx_search/ajax_results_return_research.html', context_dict)


def execute_download(request, query_id):
    
    download_request = Download_Request.objects.get(id=query_id) 
    case_query_set = download_request.case_set.cases.all()
    
    cursor = get_SQL_cursor(request)
    cursor.execute('CREATE TABLE #TEMP (temp_case_id nchar(20))')
    
    for case in case_query_set:
        query = "INSERT INTO #TEMP (temp_case_id) VALUES ('%s')" % (case.case_id)
        cursor.execute(query)

    select_substring = 'SELECT TOP(5000) case_id, age, sex, DOB, MRN, staff, specimen_class, accession_date, text, first_name, last_name, gross, clinical, synoptic, intraoperative, specimen_type '
    join_substring = 'FROM [#TEMP] JOIN dbo.ap_case on [#TEMP].temp_case_id = case_id'
    final_query_string = select_substring + join_substring 

    cursor.execute(final_query_string) 

    results = cursor.fetchall()

    cursor.execute('DROP TABLE #TEMP')

    output_results_list = []
    for i in results:

        dict = {'case_id': i[0], 'age': i[1], 'sex': i[2], 'DOB': i[3], 'MRN': i[4], 'staff': i[5], 'specimen_class': i[6], 'accession_date': i[7], 'text': i[8], 'first_name': i[9], 'last_name': i[10], 'gross': i[11],  'clinical': i[12], 'synoptic': i[13], 'intraoperative': i[14], 'specimen_type': i[15]}


        output_results_list.append(dict)

    df = dataframe_writer(output_results_list)

    df = PHI_filter(df, download_request)

    download_request.status = 'Completed'
    AddNote(request, download_request, 'Completed')
    download_request.execute_user = request.user.username
    download_request.datetime = datetime.datetime.now()
    download_request.save()

    excel_file = download_request.user.username + '.xlsx'

    file_path = os.path.join(settings.STATIC_DIR, excel_file)

    df.to_excel(file_path, index=False)

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + excel_file

        return response

# Executes predefined database query to get year and staff info.
def get_metadata(request):

    cursor = get_SQL_cursor(request)

    search_string_b = "SELECT DATEPART(yyyy, [accession_date]), count(DATEPART(yyyy, [accession_date])) FROM dbo.ap_case GROUP BY DATEPART(yyyy, [accession_date]) ORDER BY DATEPART(yyyy, [accession_date]) DESC"
    cursor.execute(search_string_b)
    
    results = cursor.fetchall()

    year_list = []
    for i in results:
        year, no_of_cases = i[0], i[1]
        year_list.append([year, no_of_cases])

    search_string_c = "SELECT staff, count(staff) from dbo.ap_case GROUP BY staff ORDER BY staff"
    cursor.execute(search_string_c)
    
    results = cursor.fetchall()

    staff_list = []
    for i in results:
        year, no_of_cases = i[0], i[1]
        staff_list.append([year, no_of_cases])

    return [year_list, staff_list]

