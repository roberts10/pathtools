from django.conf.urls import url
from dx_search import views 
from django.views.generic import TemplateView

urlpatterns = [
        url(r'^$', views.dx_search, name='dx_search'),
        url(r'^about$', views.about, name='about'),
        url(r'^execute_search_preview$', views.execute_search_preview, name='execute_search_preview'),
        url(r'^execute_search_research$', views.execute_search_research, name='execute_search_research'),
        url(r'^dx_download$', views.dx_download, name='dx_download'),
        url(r'download_request/(?P<case_set_id>\d+)/$', views.download_request, name='download_request'),
        url(r'analyst_dashboard$', views.analyst_dashboard, name='analyst_dashboard'),
        url(r'case_set_dashboard$', views.case_set_dashboard, name='case_set_dashboard'),
        url(r'change_options/(?P<query_id>\d+)/$', views.change_options, name='change_options'),
        url(r'download_request_instance_manager/(?P<query_id>\d+)/$', views.download_request_instance_manager, name='download_request_instance_manager'),
        url(r'execute_download/(?P<query_id>\d+)/$', views.execute_download, name='execute_download'),
        url(r'reject_request/(?P<query_id>\d+)/$', views.reject_request, name='reject_request'),
        url(r'pending_request/(?P<query_id>\d+)/$', views.pending_request, name='pending_request'),
        url(r'request_submitted$', views.request_submitted, name='request_submitted'), 
        url(r'case_upload_portal$', views.case_upload_portal, name='case_upload_portal'),
        url(r'^case_set_instance_manager/(?P<case_set_id>\d+)/$', views.case_set_instance_manager, name='case_set_instance_manager'),
        url(r'load_case_set_to_memory/(?P<case_set_id>\d+)/$', views.load_case_set_to_memory, name='load_case_set_to_memory'),
        url(r'capture_cases$', views.capture_cases, name='capture_cases'),
        url(r'clear_loaded_case_set', views.clear_loaded_case_set, name='clear_loaded_case_set'),
        url(r'delete_case_set/(?P<case_set_id>\d+)/$', views.delete_case_set, name='delete_case_set'),
        url(r'delete_case_set_goto_dashboard/(?P<case_set_id>\d+)/$', views.delete_case_set_goto_dashboard, name='delete_case_set_goto_dashboard'),
        url(r'patient_case_id_history_search/(?P<case_set_id>\d+)/$', views.patient_case_id_history_search, name='patient_case_id_history_search'),
        url(r'login/', views.CustomLoginView.as_view(template_name = 'registration/login.html'), name = 'login'),
        url(r'password/change_expired$', views.CustomPasswordChangeView.as_view(template_name = 'registration/expired_password_change_form.html'), name = 'password_change_expired'),
        url(r'password/change_default$', views.CustomPasswordChangeView.as_view(template_name = 'registration/password_change_form.html'), name = 'password_change_default'),
        url(r'password/change/done', views.CustomPasswordChangeDoneView.as_view(template_name = 'registration/password_change_done.html'), name = 'password_change_done'),
        ]

        
