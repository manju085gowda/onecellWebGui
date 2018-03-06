from django.conf.urls import url
import webapp.views
from webapp.views import *
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth
from django.conf.urls import (
handler400, handler403, handler404, handler500
)


handler404 = 'webapp.views.handler404'
handler500 = 'mysite.views.handler500'
#handler403 = 'mysite.views.my_custom_permission_denied_view'
#handler400 = 'mysite.views.my_custom_bad_request_view'

urlpatterns = [
    url(r'^login/$', auth.login, {'template_name': 'login.html', 'authentication_form': LoginForm},name="login"),
    url(r'^logout/$', auth.logout, {'next_page': '/login'}),
    url(r'^signin/$', webapp.views.sign_in, name='signin'),
    url(r'^wizard/$', webapp.views.render_wizard_screen, name='wizard'),
    url(r'^upload/$', webapp.views.upload_config_file, name='upload'),
    url(r'^whitelist_upload/$', webapp.views.upload_whitelist_file, name='upload_whitelist_file'),
    url(r'^ajax/validate_ipaddressform/',IPAddressFormView.as_view(),name='validate_ipaddressform'),
    url(r'^ajax/validate_frontHaulform/',FrontHaulConfigView.as_view(),name='validate_frontHaulform'),
    url(r'^ajax/validate_redundancyForm/',RedundancyFormView.as_view(),name='validate_redundancyForm'),
    url(r'^ajax/validate_nominalgps/', NominalGPSFormView.as_view(), name='validate_nominalgps'),
    url(r'^ajax/validate_boundaryclock/', BCConfigFormView.as_view(), name='validate_boundaryclock'),
    url(r'^ajax/validate_mgmtPortConfigForm/', MgmtPortConfigFormView.as_view(), name='validate_mgmtPortConfigForm'),
    url(r'^ajax/validate_hemsForm/',HemsFormView.as_view(),name='validate_hemsForm'),
    url(r'^ajax/validate_snmpForm/',SNMPFormView.as_view(),name='validate_snmpForm'),
    url(r'^ajax/validate_whitelist/', WhitelistFormView.as_view(), name='validate_whitelist'),
    url(r'^ajax/validate_license/', LicenseFormView.as_view(), name='validate_license'),
    url(r'^ajax/validate_backHaulS1/', S1ConfigView.as_view(), name='validate_backHaulS1'),
    url(r'^ajax/validate_backHaulOAM/',OAMConfigView.as_view(),name='validate_backHaulOAM'),
    url(r'^ajax/validate_backHaulS1Gateway/', S1GConfigView.as_view(), name='validate_backHaulS1Gateway'),
    url(r'^ajax/validate_backHaulOAMGateway/', OAMGConfigView.as_view(), name='validate_backHaulOAMGateway'),
    url(r'^ajax/validate_caServerForm/',CAServerFormView.as_view(),name='validate_caServerForm'),
    url(r'^deployment_quessionnaire/', DeploymentQuessionnaireView.as_view(), name='deployment_quessionnaire'),
    url(r'^summary/', TemplateView.as_view(template_name='summaryPage.html'), name='deployment_quessionnaire'),
    url(r'^applyConfiguration/$', webapp.views.apply_config, name='applyConfiguration'),
]
