# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import shutil
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import FormView

from djangoapp.settings import XSD_FILE_PATH, TEMP_FOLDER_NAME, XML_ERROR_SYNTAX_LOG_PATH, SAMPLE_CSV_TEMPLATE_PATH, \
    OPERATOR_CONFIG_FOLDER, SECGW1_PERSISTENCE_FILE, SECGW2_PERSISTENCE_FILE, STATICTIACFG1_PERSISTENCE_FILE, \
    STATICTIACFG2_PERSISTENCE_FILE, TIMING_SOURCE_PERSISTENCE_FILE, CA_SERVER_PERSISTENCE_FILE, \
    HEMSURL_PERSISTENCE_FILE, WHITELIST_PERSISTENCE_FILE, webapi, HEMSACCESS_PERSISTENCE_FILE

from webapp.forms import *
import webapp.global_dict as gd
from ajax_forms.views import AjaxFormView
from django.template import RequestContext
from collections import OrderedDict
from lxml import etree
from io import BytesIO
import json
import xmltodict
import tarfile
import zipfile
import OpenSSL.crypto
import re
from ctypes import *

from webapp.utils import call_moGet, STATICPort, ip2int, set_iface_data, MO_TYPE, call_moSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

serial_no_value = None
hw_version_value = None
sw_version_value = None


def get_device_info():
    global serial_no_value, hw_version_value, sw_version_value
    param = ["Device.DeviceInfo.SerialNumber", "6",
             "Device.DeviceInfo.HardwareVersion", "6",
             "Device.DeviceInfo.SoftwareVersion", "6"]
    ret = call_moGet(param)

    if ret == 0:
        ptr = POINTER(c_char_p * len(param)).in_dll(webapi, 'value')
        dimclient_output = []

        for i in ptr.contents:
            dimclient_output.append(i)

        serial_no_index = dimclient_output.index("Device.DeviceInfo.SerialNumber")
        serial_no_value = dimclient_output[serial_no_index + 1]
        print serial_no_value

        hw_version_index = dimclient_output.index("Device.DeviceInfo.HardwareVersion")
        hw_version_value = dimclient_output[hw_version_index + 1]
        print hw_version_value

        sw_version_index = dimclient_output.index("Device.DeviceInfo.SoftwareVersion")
        sw_version_value = dimclient_output[sw_version_index + 1]
        print sw_version_value
    else:
        print "GET failed!!!"

    return ret


# Function to render the wizard screen
@login_required(login_url="login/")
def render_wizard_screen(request):
    global root_cert_dict
    root_cert_dict = {'SerialNo': 'NA',
                      'Issuer': 'NA',
                      'Subject': 'NA',
                      'ValidFrom': 'NA',
                      'ValidTo': 'NA',
                      'Validity': 'NA'
                      }

    # Parse sample xml to build the global dictionary
    xml_to_dict(SAMPLE_CSV_TEMPLATE_PATH)

    # Get Serial Number, Hardware Version and Software Version info from dimclient (GPV)
    # get_device_info()

    # Get default interface info
    # get_iface_info()

    # Create form objects for each screen
    form_questionnaire = DeploymentQuestionnaireForm()
    form_configfile = ConfigFileUploadForm()
    form_mgmt = MgmtPortConfigForm({'Mode': 'static'})
    form_s1 = S1ConfigForm({'Mode': 'static'})
    form_oam = OAMConfigForm({'Mode': 'static'})
    form_s1G = SecGW1Form({'AddressType': 'Static', 'ExcludeCP': 'FALSE'})
    form_oamG = SecGW2Form({'AddressType': 'Static', 'ExcludeCP': 'FALSE'})
    form_bc = BCConfigForm({'Mode': 'static', 'TimingSource': 'GPS'})
    form_rdncy = RedundancyForm({'Mode': 'static', 'BCRedundancy': None, 'CUState': 'Standby'})
    form_hems = HeMSConfigForm({'HeMSAccess': 'NonIPSec'})
    form_caserver = CAServerConfigForm({'CAServerAccess': 'NonIPSec', 'NONIPSecHttps': 'FALSE'})
    form_snmp = SNMPConfigForm(
        {'SNMPTraps': False, 'USM': None, 'AuthProtocol': 'HMAC-MD5-96', 'PrivateProtocol': 'NONE'})
    form_whitelist = WhitelistForm({})
    form_license = LicenseForm({})
    form_nominalgps = NominalGPSConfigForm({'LatitudeSign': 'North', 'DirectionOfAltitude': 'Height'})
    form_fronthaul = FrontHaulConfigForm({})

    context = {
        'serial_no': serial_no_value,
        'hw_version': hw_version_value,
        'sw_version': sw_version_value,
        'form_questionnaire': form_questionnaire,
        'form_configfile': form_configfile,
        'form_mgmt': form_mgmt,
        'form_fronthaul': form_fronthaul,
        'form_rdncy': form_rdncy,
        'form_s1': form_s1,
        'form_oam': form_oam,
        'form_s1G': form_s1G,
        'form_oamG': form_oamG,
        'form_nominalgps': form_nominalgps,
        'form_bc': form_bc,
        'form_hems': form_hems,
        'form_caserver': form_caserver,
        'root_cert_dict': root_cert_dict,
        'form_snmp': form_snmp,
        'form_whitelist': form_whitelist,
        'form_license': form_license,
    }
    return render(request, 'wizard.html', context)


# Function to handle configuration file upload
@login_required(login_url="login/")
def upload_config_file(request):
    response_data = {'status': "error", 'result': "Server error"}
    result = ""
    if request.method == "POST":
        if request.is_ajax():
            print "AJAX"

            # store uploaded file in Temporary location
            store_status = store_uploaded_file(request.FILES['file'], str(request.FILES['file']), True)

            # extract compressed config file (.tar, .tar.gz, .zip)
            if store_status == 0:
                print "Storing to tmp operation success"
                extract_status = extract_config_file(TEMP_FOLDER_NAME + str(request.FILES['file']))

                if extract_status == 0:
                    print "Extract to tmp operation success"
                    xml, xml_result = process_xml_config_file(TEMP_FOLDER_NAME)

                    if xml == 0:
                        print "processing of XML file success"
                        check_filename = check_additional_filenames()
                        if check_filename == 0:
                            pem_filename = str(gd.additional_file_dict['SeGWRootCertFileName'])
                            pem, pem_result = process_pem_file(TEMP_FOLDER_NAME + pem_filename)
                            if pem == -1:
                                if not pem_result == "":
                                    result += pem_result
                            whitelist_filename = str(gd.additional_file_dict['WhitelistFileName'])
                            whitelist, whitelist_result = process_whitelist_file(TEMP_FOLDER_NAME + whitelist_filename)
                            if whitelist == -1:
                                if not whitelist_result == "":
                                    result += whitelist_result

                            if not result == "":
                                response_data['status'] = "error"
                                response_data['result'] = result
                                return HttpResponse(json.dumps(response_data), content_type="application/json")
                                # return JsonResponse(response_data, status=500)
                        else:
                            print "FileNames are not configured in XML"
                            response_data['status'] = "error"
                            response_data['result'] = "FileNames are not configured in XML"
                            return HttpResponse(json.dumps(response_data), content_type="application/json")
                            # return JsonResponse(response_data, status=500)
                    else:
                        print "Failed to process xml file"
                        response_data['status'] = "error"
                        response_data['result'] = xml_result
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                        # return JsonResponse(response_data, status=500)
                else:
                    print "Failed to extract to " + TEMP_FOLDER_NAME + " folder"
                    response_data['status'] = "error"
                    response_data['result'] = "Please upload a valid filetype(.zip/.tar.gz,.tar)"
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                    # return JsonResponse(response_data, status=500)
            else:
                print "Failed to store at " + TEMP_FOLDER_NAME + " folder"
                response_data['status'] = "error"
                response_data['result'] = "Server error"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
                # return JsonResponse(response_data, status=500)

            response_data['status'] = "success"
            response_data['result'] = "File uploaded and processed successfully"

            form_mgmt = MgmtPortConfigForm(gd.mgmt_dict)
            form_s1 = S1ConfigForm(gd.s1config_dict)
            form_s1G = SecGW1Form(gd.secgw1_dict)
            form_oam = OAMConfigForm(gd.oamconfig_dict)
            form_oamG = SecGW2Form(gd.secgw2_dict)
            form_bc = BCConfigForm(gd.bc_dict)
            form_nominalgps = NominalGPSConfigForm(gd.ngps_dict)
            form_fronthaul = FrontHaulConfigForm(gd.fh_dict)
            form_rdncy = RedundancyForm(gd.rdncy_dict)
            form_hems = HeMSConfigForm(gd.hems_dict)
            form_caserver = CAServerConfigForm(gd.caserver_dict)
            form_snmp = SNMPConfigForm(gd.snmp_dict)
            form_whitelist = WhitelistForm(gd.whitelist_config_dict)
            form_license = LicenseForm({})

            form_mgmt_html = render_to_string('managementPortConfig.html', {'form_mgmt': form_mgmt}, request=request)
            form_backhaul_html = render_to_string('backhaul.html', {'form_s1': form_s1,
                                                                    'form_oam': form_oam,
                                                                    'form_s1G': form_s1G,
                                                                    'form_oamG': form_oamG
                                                                    }, request=request)
            form_bc_html = render_to_string('boundaryClock.html', {'form_bc': form_bc,
                                                                   'form_nominalgps': form_nominalgps
                                                                   }, request=request)
            form_fronthaul_html = render_to_string('fronthaul.html', {'form_fronthaul': form_fronthaul},
                                                   request=request)
            form_rdncy_html = render_to_string('redundancy.html', {'form_rdncy': form_rdncy}, request=request)
            form_hems_html = render_to_string('hemsConfig.html', {'form_hems': form_hems}, request=request)
            form_caserver_html = render_to_string('caServerConfig.html', {'form_caserver': form_caserver},
                                                  request=request)
            root_certificate_html = render_to_string('rootCertificate.html', {'root_cert_dict': root_cert_dict},
                                                     request=request)
            form_snmp_html = render_to_string('snmp.html', {'form_snmp': form_snmp}, request=request)
            form_whitelist_html = render_to_string('whitelist.html', {'form_whitelist': form_whitelist},
                                                   request=request)
            form_license_html = render_to_string('viewapplylicense.html', {'form_license': form_license},
                                                 request=request)
            navigation_html = render_to_string('navigation.html', {'form_mgmt': form_mgmt,
                                                                   'form_s1': form_s1, 'form_oam': form_oam,
                                                                   'form_s1G': form_s1G, 'form_oamG': form_oamG,
                                                                   'form_bc': form_bc,
                                                                   'form_nominalgps': form_nominalgps,
                                                                   'form_fronthaul': form_fronthaul,
                                                                   'form_rdncy': form_rdncy,
                                                                   'form_hems': form_hems,
                                                                   'form_caserver': form_caserver,
                                                                   'form_snmp': form_snmp,
                                                                   'form_whitelist': form_whitelist,
                                                                   'form_license': form_license
                                                                   }, request=request)

            context = {
                'result': response_data['result'],
                'form_mgmt_html': form_mgmt_html,
                'form_backhaul_html': form_backhaul_html,
                'form_bc_html': form_bc_html,
                'form_fronthaul_html': form_fronthaul_html,
                'form_rdncy_html': form_rdncy_html,
                'form_hems_html': form_hems_html,
                'form_caserver_html': form_caserver_html,
                'root_certificate_html': root_certificate_html,
                'form_snmp_html': form_snmp_html,
                'form_whitelist_html': form_whitelist_html,
                'form_license_html': form_license_html,
                'navigation_html': navigation_html
            }
            return JsonResponse(context, status=200)

    return HttpResponse(json.dumps(response_data), content_type='application/json')


class PreWizardView(LoginRequiredMixin, FormView):
    template_name = "preWizard.html"
    login_url = '/login/'
    form_class = PreWizard
    success_url = '/form-success/'

    def valid_submit(self, form):
        print "valid"


class DeploymentQuessionnaireView(LoginRequiredMixin, AjaxFormView):
    form_class = DeploymentQuestionnaireForm
    template_name = 'wizard.html'
    login_url = '/login/'
    success_url = '/form-success/'

    def valid_submit(self, form):
        print "valid"
        gd.dq_response_dict = form.cleaned_data
        print gd.dq_response_dict


class IPAddressFormView(LoginRequiredMixin, AjaxFormView):
    form_class = IpAddressForm
    template_name = 'wizard.html'
    login_url = '/login/'
    success_url = '/form-success/'


class MgmtPortConfigFormView(AjaxFormView):
    form_class = MgmtPortConfigForm
    template_name = 'wizard.html'

    def valid_submit(self, form):
        gd.mgmt_dict = form.cleaned_data
        print gd.mgmt_dict


class S1ConfigView(AjaxFormView):
    form_class = S1ConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.s1config_dict = form.cleaned_data
        print gd.s1config_dict


class S1GConfigView(AjaxFormView):
    form_class = SecGW1Form
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.secgw1_dict = form.cleaned_data
        print gd.secgw1_dict


class OAMConfigView(AjaxFormView):
    form_class = OAMConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.oamconfig_dict = form.cleaned_data
        print gd.oamconfig_dict


class OAMGConfigView(AjaxFormView):
    form_class = SecGW2Form
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.secgw2_dict = form.cleaned_data
        print gd.secgw2_dict


class BCConfigFormView(AjaxFormView):
    form_class = BCConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.bc_dict = form.cleaned_data
        print gd.bc_dict


class NominalGPSFormView(AjaxFormView):
    form_class = NominalGPSConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.ngps_dict = form.cleaned_data
        print gd.ngps_dict


class FrontHaulConfigView(AjaxFormView):
    form_class = FrontHaulConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.fh_dict = form.cleaned_data
        print gd.fh_dict


class RedundancyFormView(AjaxFormView):
    form_class = RedundancyForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.rdncy_dict = form.cleaned_data
        print gd.rdncy_dict


class HemsFormView(AjaxFormView):
    form_class = HeMSConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.hems_dict = form.cleaned_data
        print gd.hems_dict


class CAServerFormView(AjaxFormView):
    form_class = CAServerConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.caserver_dict = form.cleaned_data
        print gd.caserver_dict


class SNMPFormView(AjaxFormView):
    form_class = SNMPConfigForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.snmp_dict = form.cleaned_data
        print gd.snmp_dict


class WhitelistFormView(AjaxFormView):
    form_class = WhitelistForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        gd.whitelist_config_dict = form.cleaned_data
        print gd.whitelist_config_dict


class LicenseFormView(AjaxFormView):
    form_class = LicenseForm
    template_name = 'wizard.html'
    success_url = '/form-success/'

    def valid_submit(self, form):
        print "valid"


# Function to parse xml file and create a global dictionary
def xml_to_dict(xml_path):
    try:
        with open(xml_path, 'r') as xml_file:
            xml_to_check = xml_file.read()
        gd.parsed_dict = xmltodict.parse(xml_to_check)
        print gd.parsed_dict

        gd.mgmt_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.MANAGEMENT_INTERFACE_XML_STRING]
        gd.s1config_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.S1_CONFIG_XML_STRING]
        gd.secgw1_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.SECGW1_CONFIG_XML_STRING]
        gd.oamconfig_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.OAM_CONFIG_XML_STRING]
        gd.secgw2_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.SECGW2_CONFIG_XML_STRING]
        gd.bc_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.BOUNDARY_CLOCK_CONFIG_XML_STRING]
        gd.ngps_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.NOMINAL_GPS_CONFIG_XML_STRING]
        gd.fh_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.FRONTHAUL_CONFIG_XML_STRING]
        gd.rdncy_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.PORT_CONFIG_XML_STRING][
            gd.REDUNDANCY_CONFIG_XML_STRING]
        gd.hems_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.OPERATOR_CONFIG_XML_STRING][
            gd.HEMS_CONFIG_XML_STRING]
        gd.caserver_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.OPERATOR_CONFIG_XML_STRING][
            gd.CA_SERVER_CONFIG_XML_STRING]
        gd.snmp_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.SNMP_CONFIG_XML_STRING]
        gd.user_config_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.USER_CONFIG_XML_STRING]
        gd.whitelist_config_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.WHITELIST_CONFIG_XML_STRING]
        gd.additional_file_dict = gd.parsed_dict[gd.ONECELL_PROFILE_XML_STRING][gd.ADDITIONAL_FILENAMES_XML_STRING]

    except IOError:
        print "Could not read file " + xml_path

    except KeyError as e:
        print "Key " + '\"' + e.args[0] + '\"' + " not found"


def check_additional_filenames():
    try:
        gd.parsed_dict['OneCell-Config-Profile']['Additional-FileNames-Included']
    except Exception as e:
        print "FileNames are not configured in xml" + e.message
        return -1
    return 0


def upload_whitelist_file(request):
    response_data = {'status': "error", 'result': "Server error"}
    if request.method == "POST":
        if request.is_ajax():
            print "AJAX"

            # store uploaded file in Temporary location
            store_status = store_uploaded_file(request.FILES['whitelist_file'], str(request.FILES['whitelist_file']),
                                               False)
            if store_status == 0:
                print TEMP_FOLDER_NAME + str(request.FILES['whitelist_file'])
                whitelist_status, whitelist = process_whitelist_file(
                    TEMP_FOLDER_NAME + str(request.FILES['whitelist_file']))
                print whitelist
                if whitelist_status == 0:
                    print "processing of whitelist file success"
                    gd.whitelist_config_dict['Whitelist'] = whitelist
                    print "Success"
                    response_data['status'] = "success"
                    response_data['result'] = whitelist
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                else:
                    print "processing of whitelist file failed"
                    response_data['status'] = "error"
                    response_data['result'] = whitelist
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                print "Failed to store Whitelist file"
                response_data['status'] = "error"
                response_data['result'] = "Failed to store Whitelist file"
                return HttpResponse(json.dumps(response_data), content_type="application/json")

    return HttpResponse(json.dumps(response_data), content_type="application/json")


# Function to store uploaded .tar, .tar.gz, .zip to temporary location "/tmp/"
def store_uploaded_file(file, filename, isClear):
    if not os.path.exists(TEMP_FOLDER_NAME):
        os.mkdir(TEMP_FOLDER_NAME)
    else:
        if isClear:
            clear_tmp_content()
    try:
        with open(TEMP_FOLDER_NAME + filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return 0
    except IOError:
        print "Could not copy uploaded file " + filename
        return -1


def clear_tmp_content():
    for the_file in os.listdir(TEMP_FOLDER_NAME):
        file_path = os.path.join(TEMP_FOLDER_NAME, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def extract_config_file(filepath):
    if filepath.endswith("tar.gz"):
        tar = tarfile.open(filepath, "r:gz")
        tar.extractall(TEMP_FOLDER_NAME)
        tar.close()
        return 0
    elif filepath.endswith("tar"):
        tar = tarfile.open(filepath, "r:")
        tar.extractall(TEMP_FOLDER_NAME)
        tar.close()
        return 0
    elif filepath.endswith("zip"):
        tar = zipfile.ZipFile(filepath, 'r')
        tar.extractall(TEMP_FOLDER_NAME)
        tar.close()
        return 0
    else:
        return -1


# Function to process xml file
def process_xml_config_file(path):
    print "process_xml_config_file"
    # xsd validation
    xml_isexist = False
    for the_file in os.listdir(path):
        if "onecell-config.xml" in the_file:
            xml_isexist = True
            xml_file_path = path + the_file
            try:
                with open(XSD_FILE_PATH, 'r') as schema_file:
                    schema_to_check = schema_file.read()

                with open(xml_file_path, 'r') as xml_file:
                    xml_to_check = xml_file.read()

                xmlschema_doc = etree.parse(BytesIO(schema_to_check))
                xmlschema = etree.XMLSchema(xmlschema_doc)

                doc = etree.parse(BytesIO(xml_to_check))
                print('XML well formed, syntax ok.')
                # try:
                #    xmlschema.assertValid(doc)
                #    print('XML valid, schema validation ok.')

                # except etree.DocumentInvalid as err:
                #    print('Schema validation error, see error_schema.log')
                #    with open(TEMP_FOLDER_NAME + 'error_schema.log', 'w') as error_log_file:
                #        error_log_file.write(str(err.error_log))
                #        error_log_file.close()
                #
                #    return -1, "XML validation failed"
                #    # quit()
                # except Exception as e:
                #    print('Unknown error, exiting.' + e.message)
                #    return -1, "XML validation failed"
                # quit()

                # if xsd validation is success, parse xml and store in global dictionary
                xml_to_dict(xml_file_path)
                # gd.parsed_dict = xmltodict.parse(xml_to_check)

                print gd.parsed_dict
                update_dictionary_with_dq_response()
                print "UPDATED!"
                print gd.parsed_dict
            # check for file IO error
            except IOError as e:
                print('Invalid File' + e.message)
            # check for XML syntax errors
            except etree.XMLSyntaxError as err:
                print('XML Syntax Error, see error_syntax.log')
                with open(XML_ERROR_SYNTAX_LOG_PATH, 'w') as error_log_file:
                    error_log_file.write(str(err.error_log))
                    error_log_file.close()
                    # show error on html
                    return -1, "XML syntax is not proper"
                # quit()
            except Exception as e:
                print('Unknown error, exiting. ' + e.message)
                return -1, "XML syntax is not proper"
                # quit()
    if not xml_isexist:
        print "xml file not found"
        return -1, "xml file not found - please include 'onecell-config.xml'"
    return 0, ""


# process ".pem" files
def process_pem_file(file):
    try:
        st_cert = open(file, 'rt').read()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, st_cert)
        global root_cert_dict
        root_cert_dict = OrderedDict()
        root_cert_dict['SerialNo'] = str(cert.get_serial_number())
        root_cert_dict[
            'Issuer'] = "/C= " + cert.get_issuer().countryName + "/ST= " + cert.get_issuer().stateOrProvinceName + "/O= " + cert.get_issuer().organizationName + "/OU= " + cert.get_issuer().organizationalUnitName + "/CN= " + cert.get_issuer().commonName  # + "/L= " + cert.get_issuer().localityName
        root_cert_dict[
            'Subject'] = "/C= " + cert.get_subject().countryName + "/ST= " + cert.get_subject().stateOrProvinceName + "/O= " + cert.get_subject().organizationName + "/OU= " + cert.get_subject().organizationalUnitName + "/CN= " + cert.get_subject().commonName  # + "/L= " + cert.get_subject().localityName
        root_cert_dict['ValidFrom'] = str(cert.get_notBefore())
        root_cert_dict['ValidTo'] = str(cert.get_notAfter())
        root_cert_dict['Validity'] = str(cert.has_expired())
        print "Root Cert data:" + str(root_cert_dict)
    except Exception as e:
        print "Error while processing pem" + e.message
        return -1, "<p>pem file - " + pem_filename + " configured in xml does not exist</p>"
    return 0, ""


# process whitelist data
def process_whitelist_file(filepath):
    try:
        whitelist_string = open(filepath, 'rt').read()
        print whitelist_string
        ret, ret_reason = validate_whitelist(whitelist_string)
    except Exception as e:
        return -1, "<p>whitelist file - " + whitelist_filename + " configured in xml does not exist</p>"
    return ret, ret_reason


# validate whitelist data
def validate_whitelist(whitelist):
    whitelist_regex = "(((\\;){0,1}([0-9a-fA-F]{12}))|(([0-9a-fA-F]{4,12})(\\;)([0-9a-fA-F]{12}){0,1}))" + "(((,)(\\;){0,1}[0-9a-fA-F]{12})|((,)[0-9a-fA-F]{12}(\\;)([0-9a-fA-F]{12}){0,1}))*\Z"
    result = re.match(whitelist_regex, whitelist)
    # print result
    if result is not None:
        print "Whitelist is valid"
        return 0, whitelist
    else:
        print "Whitelist is invalid"
        scenario_list = []
        invalid_scenarios = [";;", ",,", ",;,"]
        for scenario in invalid_scenarios:
            if scenario in whitelist:
                print scenario
                scenario = " " + scenario + " "
                scenario_list.append(scenario.encode("utf-8"))
        if len(scenario_list) > 0:
            return -1, "<p> Whitelist is invalid- please check for following invalid pattern - " + str(
                scenario_list) + " </p>"
        else:
            return -1, "<p> Whitelist is invalid </p>"


def update_dictionary_with_dq_response():
    if gd.dq_response_dict['bc_hems_communication'] == 'S1' or gd.dq_response_dict['bc_hems_communication'] == 'OAM':
        gd.hems_dict['HeMSAccess'] = 'IPSec'
    if gd.dq_response_dict['bc_ca_communication'] == 'S1' or gd.dq_response_dict['bc_ca_communication'] == 'OAM':
        gd.caserver_dict['CAServerAccess'] = 'IPSec'

    if gd.dq_response_dict['bc_timing'] != gd.bc_dict['TimingSource']:
        gd.bc_dict['TimingSource'] = gd.dq_response_dict['bc_timing']

    if gd.dq_response_dict['bc_redundancy_enable'] != gd.rdncy_dict['BCRedundancy']:
        gd.rdncy_dict['BCRedundancy'] = gd.dq_response_dict['bc_redundancy_enable']

    return 0


def apply_all_config():
    whitelist_data = gd.whitelist_config_dict[gd.WHITELIST_STRING]

    network_status = apply_network_config()
    operator_status = apply_operator_config()
    snmp_status = apply_snmp_config()  # done
    user_status = apply_user_config()  # TBD
    white_status = apply_whitelist_config(whitelist_data)  # done

    if gd.dq_response_dict['bc_mme_communication'] == 'S1' and gd.dq_response_dict['bc_hems_communication'] == 'OAM':
        reboot_BC()
    return 0


def apply_network_config():
    # Check for BC and Rdncy options in DQ
    iface_status = apply_interface_config()

    # Check MME and HeMS options
    secgw_status = apply_secgw_config()
    stia_status = apply_statictia_config()

    # Check MME, HeMS and Timing source-BC port option
    # if dual ipsec is enabled execute vitesse script (/usr/bin/cu-port-config.sh)
    vitesse_status = apply_vitesse_config()

    # always
    timing_status = apply_timing_source()

    # Do only if Timing Source is PTP
    if gd.dq_response_dict['bc_timing'] == 'PTP':
        ptp_status = apply_ptp_servers()
        ngps_status = apply_ngps_config()

    # always
    fh_status = apply_fronthaul_config()

    # if DQ redundancy is yes apply, else dont apply
    if gd.dq_response_dict['bc_redundancy_enable'] == 'Yes':
        rdncy_status = apply_redundancy_config()

    return 0


def fill_iface_data(iface):
    filled_data = STATICPort()
    filled_data.IPAddr = ip2int(iface[gd.IPADDRESS_XML_STRING])
    filled_data.Mask = int(iface[gd.SUBNETMASK_XML_STRING])
    filled_data.GW = ip2int(iface[gd.DEFAULTGW_XML_STRING])
    filled_data.DNSPri = ip2int(iface[gd.PRIDNS_XML_STRING])
    filled_data.DNSSec = ip2int(iface[gd.SECDNS_XML_STRING])
    filled_data.DhcpEnable = 0 if iface[gd.IFACE_MODE_XML_STRING].lower() == 'static' else 1
    return filled_data


def apply_interface_config():
    mgmt_ret, ipsec_ret, timing_ret, bc_ret, ipsec2_ret, rdncy_ret = 0
    mgmt_iface_data = fill_iface_data(gd.mgmt_dict)
    mgmt_ret = set_iface_data(mgmt_iface_data)

    ipsec_iface_data = fill_iface_data(gd.s1config_dict)
    ipsec_ret = set_iface_data(ipsec_iface_data)

    # timing_iface_data = fill_iface_data()
    # timing_ret = set_iface_data(timing_iface_data)

    if gd.dq_response_dict['bc_timing'] == 'PTP':
        bc_iface_data = fill_iface_data(gd.bc_dict)
        bc_ret = set_iface_data(bc_iface_data)

    if gd.dq_response_dict['bc_mme_communication'] == 'S1' and gd.dq_response_dict['bc_hems_communication'] == 'OAM':
        ipsec2_iface_data = fill_iface_data(gd.oamconfig_dict)
        ipsec2_ret = set_iface_data(ipsec2_iface_data)

    if gd.dq_response_dict['bc_redundancy_enable'] == 'Yes':
        rdncy_iface_data = fill_iface_data(gd.rdncy_dict)
        rdncy_ret = set_iface_data(rdncy_iface_data)

    # TODO: handle error cases
    return 0


def apply_secgw_config():
    ret_secgw1, ret_secgw2 = 0
    secgw1_data = gd.secgw1_dict[gd.SECGWURL_XML_STRING]
    if not os.path.exists(OPERATOR_CONFIG_FOLDER):
        os.mkdir(OPERATOR_CONFIG_FOLDER)

    try:
        secgw1_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, SECGW1_PERSISTENCE_FILE)
        f = open(secgw1_file_path, "w+")
        f.write(secgw1_data)
        f.close()
    except IOError:
        return -1

    secgw1_mo = ["Device.Services.FAPService.1.FAPControl.LTE.Gateway.SecGWServer1", secgw1_data, MO_TYPE.STRING]

    ret_secgw1 = call_moSet(secgw1_mo)
    if ret_secgw1 == 0:
        print "Set successful"
    else:
        print "Set failed!"

    if gd.dq_response_dict['bc_mme_communication'] == 'S1' and gd.dq_response_dict['bc_hems_communication'] == 'OAM':
        secgw2_data = gd.secgw2_dict[gd.SECGWURL_XML_STRING]
        try:
            secgw2_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, SECGW2_PERSISTENCE_FILE)
            f = open(secgw2_file_path, "w+")
            f.write(secgw2_data)
            f.close()

        except IOError:
            return -1

        secgw2_mo = ["Device.Services.FAPService.1.FAPControl.LTE.Gateway.X_0005B9_SecGW2Server1", secgw2_data,
                     MO_TYPE.STRING]

        ret_secgw2 = call_moSet(secgw2_mo)
        if ret_secgw2 == 0:
            print "Set successful"
        else:
            print "Set failed!"

    return ret_secgw1, ret_secgw2


def apply_statictia_config():
    secgw1_data = gd.secgw1_dict
    if not os.path.exists(OPERATOR_CONFIG_FOLDER):
        os.mkdir(OPERATOR_CONFIG_FOLDER)

    if secgw1_data[gd.EXCLUDE_CP_XML_STRING].lower() == "true":
        secgw1_data[gd.EXCLUDE_CP_XML_STRING] = "TRUE"
    elif secgw1_data[gd.EXCLUDE_CP_XML_STRING].lower() == "false":
        secgw1_data[gd.EXCLUDE_CP_XML_STRING] = "FALSE"
    else:
        print "Invalid exclude cp option"
        return -1

    address_type = secgw1_data[gd.ADDRESS_TYPE_XML_STRING]
    internal_address = secgw1_data[gd.INTERNAL_ADDRESS_XML_STRING]
    internal_netmask = secgw1_data[gd.INTERNAL_NETMASK_XML_STRING]
    internal_dns = secgw1_data[gd.INTERNAL_DNS_XML_STRING]
    exclude_cp = secgw1_data[gd.EXCLUDE_CP_XML_STRING]

    if address_type.lower() == "static":
        try:
            statictia1_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, STATICTIACFG1_PERSISTENCE_FILE)
            f = open(statictia1_file_path, "w+")
            f.write(gd.ADDRESS_TYPE_XML_STRING + "=" + address_type)
            f.write(gd.INTERNAL_ADDRESS_XML_STRING + "=" + internal_address)
            f.write(gd.INTERNAL_NETMASK_XML_STRING + "=" + internal_netmask)
            f.write(gd.INTERNAL_DNS_XML_STRING + "=" + internal_dns)
            f.write(gd.EXCLUDE_CP_XML_STRING + "=" + exclude_cp)
            f.close()
        except IOError:
            return -1
    elif address_type.lower() == "dynamic":
        try:
            statictia1_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, STATICTIACFG1_PERSISTENCE_FILE)
            f = open(statictia1_file_path, "w+")
            f.write(gd.ADDRESS_TYPE_XML_STRING + "=" + address_type)
            f.write(gd.EXCLUDE_CP_XML_STRING + "=" + exclude_cp)
            f.close()
        except IOError:
            return -1

    secgw1_mo = ["Device.IP.Interface.1.IPv4Address.2.IPAddress", internal_address, MO_TYPE.STRING,
                 "Device.IP.Interface.1.IPv4Address.2.SubnetMask", internal_netmask, MO_TYPE.STRING,
                 "Device.IP.Interface.1.IPv4Address.2.X_0005B9_DNS", internal_dns, MO_TYPE.STRING,
                 "Device.IPsec.X_0005B9_ExcludeCP", exclude_cp, MO_TYPE.BOOLEAN,
                 "Device.IP.Interface.1.IPv4Address.2.AddressingType", address_type, MO_TYPE.STRING
                 ]

    ret = call_moSet(secgw1_mo)
    if ret == 0:
        print "Set successful"
    else:
        print "Set failed!"

    # return ret

    if gd.dq_response_dict['bc_mme_communication'] == 'S1' and gd.dq_response_dict['bc_hems_communication'] == 'OAM':
        secgw2_data = gd.secgw2_dict

        if secgw2_data[gd.EXCLUDE_CP_XML_STRING].lower() == "true":
            secgw2_data[gd.EXCLUDE_CP_XML_STRING] = "TRUE"
        elif secgw2_data[gd.EXCLUDE_CP_XML_STRING].lower() == "false":
            secgw2_data[gd.EXCLUDE_CP_XML_STRING] = "FALSE"
        else:
            print "Invalid exclude cp2 option"
            return -1

        address_type2 = secgw2_data[gd.ADDRESS_TYPE_XML_STRING]
        internal_address2 = secgw2_data[gd.INTERNAL_ADDRESS_XML_STRING]
        internal_netmask2 = secgw2_data[gd.INTERNAL_NETMASK_XML_STRING]
        internal_dns2 = secgw2_data[gd.INTERNAL_DNS_XML_STRING]
        exclude_cp2 = secgw2_data[gd.EXCLUDE_CP_XML_STRING]

        statictia2_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, STATICTIACFG2_PERSISTENCE_FILE)
        if address_type2.lower() == "static":
            try:
                f = open(statictia2_file_path, "w+")
                f.write(gd.ADDRESS_TYPE_XML_STRING + "=" + address_type2)
                f.write(gd.INTERNAL_ADDRESS_XML_STRING + "=" + internal_address2)
                f.write(gd.INTERNAL_NETMASK_XML_STRING + "=" + internal_netmask2)
                f.write(gd.INTERNAL_DNS_XML_STRING + "=" + internal_dns2)
                f.write(gd.EXCLUDE_CP_XML_STRING + "=" + exclude_cp2)
                f.close()
            except IOError:
                return -1
        elif address_type.lower() == "dynamic":
            try:
                f = open(statictia2_file_path, "w+")
                f.write(gd.ADDRESS_TYPE_XML_STRING + "=" + address_type2)
                f.write(gd.EXCLUDE_CP_XML_STRING + "=" + exclude_cp2)
                f.close()
            except IOError:
                return -1

        secgw2_mo = ["Device.IP.Interface.1.IPv4Address.3.IPAddress", internal_address2, MO_TYPE.STRING,
                     "Device.IP.Interface.1.IPv4Address.3.SubnetMask", internal_netmask2, MO_TYPE.STRING,
                     "Device.IP.Interface.1.IPv4Address.3.X_0005B9_DNS", internal_dns2, MO_TYPE.STRING,
                     "Device.X_00005B9_IPsec2.X_0005B9_ExcludeCP", exclude_cp2, MO_TYPE.BOOLEAN,
                     "Device.IP.Interface.1.IPv4Address.3.AddressingType", address_type2, MO_TYPE.STRING
                     ]

        ret = call_moSet(secgw2_mo)
        if ret == 0:
            print "Set successful"
        else:
            print "Set failed!"

    return ret


def apply_vitesse_config():
    pass


# Device.Time.X_0005B9_PTP.Server, string,  Device.Time.X_0005B9_TimeSource, string
def apply_timing_source():
    timing_data = gd.bc_dict[gd.TIMING_SOURCE_XML_STRING]

    if timing_data.lower() == "gps":
        timing_data = "GPS"
    elif timing_data.lower() == "ptp":
        timing_data = "PTP"
    else:
        print "invalid timing source"
        return -1

    timing_mo = ["Device.Time.X_0005B9_TimeSource", timing_data, MO_TYPE.STRING]

    ret = call_moSet(timing_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_ptp_servers():
    ptpserver_data = gd.bc_dict[gd.PTPSERVERS_XML_STRING]
    ptpserver_mo = ["Device.Time.X_0005B9_PTP.Server", ptpserver_data, MO_TYPE.STRING]

    ret = call_moSet(ptpserver_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_ngps_config():
    ngps_data = gd.ngps_dict
    ngps_mo = ["Device.FAP.GPS.X_0005B9_NominalGPS.LatitudeSign", ngps_data[gd.LATITUDESIGN_XML_STRING], MO_TYPE.STRING,
               "Device.FAP.GPS.X_0005B9_NominalGPS.DegreesOfLatitude", ngps_data[gd.DEGREESOFLATITUDE_XML_STRING],
               MO_TYPE.UINT,
               "Device.FAP.GPS.X_0005B9_NominalGPS.DegreesOfLongitude", ngps_data[gd.DEGREESOFLONGITUDE_XML_STRING],
               MO_TYPE.INT,  # 7
               "Device.FAP.GPS.X_0005B9_NominalGPS.DirectionOfAltitude", ngps_data[gd.DIRECTIONOFALTITUDE_XML_STRING],
               MO_TYPE.STRING,
               "Device.FAP.GPS.X_0005B9_NominalGPS.Altitude", ngps_data[gd.ALTITUDE_XML_STRING], MO_TYPE.UINT,
               "Device.FAP.GPS.X_0005B9_NominalGPS.UncertaintySemiMajor",
               ngps_data[gd.UNCERTAINITYSEMIMAJOR_XML_STRING], MO_TYPE.UINT,
               "Device.FAP.GPS.X_0005B9_NominalGPS.UncertaintySemiMinor",
               ngps_data[gd.UNCERTAINITYSEMIMINOR_XML_STRING], MO_TYPE.UINT,
               "Device.FAP.GPS.X_0005B9_NominalGPS.UncertaintyAltitude", ngps_data[gd.UNCERTAINITYALTITUDE_XML_STRING],
               MO_TYPE.UINT,
               "Device.FAP.GPS.X_0005B9_NominalGPS.OrientationOfMajorAxis", ngps_data[gd.ORIENTATIONMAJOR_XML_STRING],
               MO_TYPE.UINT,
               "Device.FAP.GPS.X_0005B9_NominalGPS.Confidence", ngps_data[gd.CONFIDENCE_XML_STRING], MO_TYPE.UINT,
               ]

    ret = call_moSet(ngps_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_fronthaul_config():
    fh_data = gd.fh_dict
    fh_mo = ["Device.FAP.X_0005B9_RUStartIp", "", MO_TYPE.STRING,
             "Device.FAP.X_0005B9_RUEndIp", "", MO_TYPE.STRING,
             "Device.FAP.X_0005B9_RUNetMask", "", MO_TYPE.STRING,
             "Device.FAP.X_0005B9_MultiCastCUGroupId", fh_data[gd.BCID_XML_STRING], MO_TYPE.UINT,
             "Device.FAP.X_0005B9_ClusterVlanId", fh_data[gd.VLANID_XML_STRING], MO_TYPE.UINT,
             ]

    ret = call_moSet(fh_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_redundancy_config():
    # TODO: cluster validation
    rdncy_data = gd.rdncy_dict

    if rdncy_data[gd.CUSTATE_XML_STRING].lower() == "active":
        rdncy_data[gd.CUSTATE_XML_STRING] = 1
    elif rdncy_data[gd.CUSTATE_XML_STRING].lower() == "standby":
        rdncy_data[gd.CUSTATE_XML_STRING] = 0
        rdncy_data[gd.VCID_XML_STRING] = "NONE"
    else:
        print "invalid cu state option"
        return -1

    if rdncy_data[gd.BCREDUNDANCY_XML_STRING].lower() == "enable":
        rdncy_data[gd.BCREDUNDANCY_XML_STRING] = 1
    elif rdncy_data[gd.BCREDUNDANCY_XML_STRING].lower() == "disable":
        rdncy_data[gd.BCREDUNDANCY_XML_STRING] = 0
    else:
        print "invalid redundancy enable option"
        return -1

    rdncy_mo = ["Device.FAP.X_0005B9_Redundancy.VIDGui", rdncy_data[gd.VCID_XML_STRING], MO_TYPE.STRING,
                "Device.FAP.X_0005B9_Redundancy.State", rdncy_data[gd.CUSTATE_XML_STRING], MO_TYPE.UINT,
                "Device.FAP.X_0005B9_Redundancy.EnableGui", rdncy_data[gd.BCREDUNDANCY_XML_STRING], MO_TYPE.BOOLEAN,
                ]

    ret = call_moSet(rdncy_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


# SPV Device.ManagementServer.URL, Device.IPsec.X_0005B9_HeMSAccess

def apply_hems_config():
    hems_data = gd.hems_dict
    if not os.path.exists(OPERATOR_CONFIG_FOLDER):
        os.mkdir(OPERATOR_CONFIG_FOLDER)

    hemsurl_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, HEMSURL_PERSISTENCE_FILE)
    hemsaccess_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, HEMSACCESS_PERSISTENCE_FILE)
    try:
        f = open(hemsurl_file_path, "w+")
        f.write(hems_data['HeMSURL'])
        f.close()

        f = open(hemsaccess_file_path, "w+")
        f.write(hems_data['HeMSAccess'])
        f.close()
    except IOError:
        return -1

    hems_mo = ["Device.ManagementServer.URL", hems_data['HeMSURL'], MO_TYPE.STRING,
               "Device.IPsec.X_0005B9_HeMSAccess", hems_data['UserName'], MO_TYPE.STRING
               ]

    ret = call_moSet(hems_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_ca_config():
    ca_data = gd.caserver_dict

    if not os.path.exists(OPERATOR_CONFIG_FOLDER):
        os.mkdir(OPERATOR_CONFIG_FOLDER)

    ca_file_path = os.path.join(OPERATOR_CONFIG_FOLDER, CA_SERVER_PERSISTENCE_FILE)
    try:
        f = open(ca_file_path, "w+")
        for key, value in ca_data.iteritems():
            f.write(key + "=" + value + "\n")
        f.close()
    except IOError:
        return -1

    if ca_data['NONIPSecHttps'].lower() == "true":
        ca_data['NONIPSecHttps'] = 1
    elif ca_data['NONIPSecHttps'].lower() == "false":
        ca_data['NONIPSecHttps'] = 0
    else:
        print "invalid non ipsec https option"
        return -1

    ca_mo = ["Device.Security.X_0005B9_CMPv2.CAServerGui", ca_data['CAServer'], MO_TYPE.STRING,
             "Device.Security.X_0005B9_CMPv2.CAServerIdentityGui", ca_data['CAServerIdentity'], MO_TYPE.STRING,
             "Device.Security.X_0005B9_CMPv2.CAServerUriGui", ca_data['CAServerURI'], MO_TYPE.STRING,
             "Device.Security.X_0005B9_CMPv2.CAServerAccessGui", ca_data['CAServerAccess'], MO_TYPE.STRING,
             "Device.Security.X_0005B9_CMPv2.CAServerPortGui", ca_data['CAServerPort'], MO_TYPE.UINT,
             "Device.Security.X_0005B9_CMPv2.NonIpsecHttps", ca_data['NONIPSecHttps'], MO_TYPE.BOOLEAN,
             "Device.Security.X_0005B9_CMPv2.SACertificateIdentifierGui", ca_data['SACertificateIdentifier'],
             MO_TYPE.STRING,
             "Device.Security.X_0005B9_CMPv2.PKIMessageHashGui", ca_data['PKIMessageHash'], MO_TYPE.STRING,
             ]

    ret = call_moSet(ca_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_root_cert_config():
    pass


def apply_operator_config():
    hems_status = apply_hems_config()

    if gd.dq_response_dict['bc_ca_communication'] != 'None':
        ca_status = apply_ca_config()

    # Do only if user has uploaded root_cert
    root_status = apply_root_cert_config()
    return 0


def apply_snmp_config():
    snmp_data = gd.snmp_dict
    if snmp_data['SNMPTraps'].lower() == "enable":
        snmp_data['SNMPTraps'] = 1
    elif snmp_data['SNMPTraps'].lower() == "disable":
        snmp_data['SNMPTraps'] = 0
    else:
        print "invalid snmp trap option"
        return -1

    if snmp_data['AuthProtocol'].lower() == "hmac-md5-96":
        snmp_data['AuthProtocol'] = 1
    elif snmp_data['AuthProtocol'].lower() == "hmac-sha-96":
        snmp_data['AuthProtocol'] = 2
    else:
        print "invalid snmp auth protocol option"
        return -1

    if snmp_data['PrivateProtocol'].lower() == "none":
        snmp_data['PrivateProtocol'] = 0
    elif snmp_data['PrivateProtocol'].lower() == "cbc-des":
        snmp_data['PrivateProtocol'] = 2
    else:
        print "invalid snmp privste protocol option"
        return -1

    if snmp_data['USM'].lower() == "yes":
        snmp_data['USM'] = 1
    elif snmp_data['USM'].lower() == "no":
        snmp_data['USM'] = 0
    else:
        print "invalid snmp usm option"
        return -1

    snmp_mo = ["Device.X_0005B9_SNMPconfig.SNMPIpAddress", snmp_data['SNMPIP'], MO_TYPE.STRING,
               "Device.X_0005B9_SNMPconfig.SNMPUsername", snmp_data['UserName'], MO_TYPE.STRING,
               "Device.X_0005B9_SNMPconfig.SNMPAuthPassPhrase", snmp_data['AuthKey'], MO_TYPE.STRING,
               "Device.X_0005B9_SNMPconfig.SNMPEncryptionPassPhrase", snmp_data['PrivateKey'], MO_TYPE.STRING,
               "Device.X_0005B9_SNMPconfig.SNMPGlobalFlag", snmp_data['SNMPTraps'], MO_TYPE.UINT,
               "Device.X_0005B9_SNMPconfig.SNMPPort", snmp_data['SNMPPort'], MO_TYPE.UINT,
               "Device.X_0005B9_SNMPconfig.SNMPAuthMethod", snmp_data['AuthProtocol'], MO_TYPE.UINT,
               "Device.X_0005B9_SNMPconfig.SNMPEncryptionMethod", snmp_data['PrivateProtocol'], MO_TYPE.UINT,
               "Device.X_0005B9_SNMPconfig.SNMPUsmEnable", snmp_data['USM'], MO_TYPE.UINT
               ]

    ret = call_moSet(snmp_mo)
    if ret == 0:
        print "Set successfull"
    else:
        print "Set failed!"

    return ret


def apply_user_config():
    return 0


def apply_whitelist_config(whitelist_data):
    if whitelist_data == "":
        print "whitelist is empty, exiting.."
        return 0

    whitelist_mo = ["Device.FAP.X_0005B9_RUWhiteList", whitelist_data, MO_TYPE.STRING]
    whitelist_fpath = TEMP_FOLDER_NAME + gd.additional_file_dict['WhitelistFileName']

    if gd.rdncy_dict[gd.BCREDUNDANCY_XML_STRING].lower() == 'enable':  # dict or get from GPV?
        if whitelist_data.lower() != 'none':
            ret = webapi.initializeSocketAndFillingStructureWithWhitelist(whitelist_data)

            if ret == 0:
                ret1 = call_moSet(whitelist_mo)
                if ret1 == 0:
                    print "whitelist set successful"
                    if os.path.exists(whitelist_fpath):
                        os.remove(whitelist_fpath)
                    return ret1
                else:
                    if os.path.exists(whitelist_fpath):
                        os.remove(whitelist_fpath)
                    print "whitelist set failed!"
                    return ret1
            else:
                print "whitelist cluster validation failed, ret = " + ret
                return ret
    else:
        ret1 = call_moSet(whitelist_mo)
        if ret1 == 0:
            if os.path.exists(whitelist_fpath):
                os.remove(whitelist_fpath)
            print "whitelist set successful"
            return ret1
        else:
            if os.path.exists(whitelist_fpath):
                os.remove(whitelist_fpath)
            print "whitelist set failed!"
            return ret1

    return 0


def reboot_BC():
    pass


def get_applied_license_info():
    appliedMO = ["Device.X_0005B9_License.X_0005B9_License.NoOfAppliedLicenses", MO_TYPE.UINT]

    root_str = "Device.X_0005B9_License.AppliedLicenses."
    child_mo = [".FeatureName", MO_TYPE.STRING,
                ".NumberOfUnits", MO_TYPE.BOOLEAN,
                ".DateTime", MO_TYPE.DATETIME,
                ".IsTemporary", MO_TYPE.UINT,
                ".TemporaryExpiryDate", MO_TYPE.DATETIME]

    # No of Applied License
    ret = call_moGet(appliedMO)
    print ret

    if ret == 0:
        l = POINTER(c_char_p * len(appliedMO)).in_dll(webapi, 'value')
        apply_output = []

        for i in l.contents:
            apply_output.append(i)

        no_of_apply_index = apply_output.index("Device.X_0005B9_License.X_0005B9_License.NoOfAppliedLicenses")
        no_of_apply_value = apply_output[no_of_apply_index + 1]
        print no_of_apply_value
        count = int(no_of_apply_value)

    else:
        print "GET failed!!!"

    # Form complete list of MOs
    mo_list = []

    for i in range(1, int(no_of_apply_value) + 1):
        sub_mo = root_str + str(i)
        for j in range(len(child_mo)):
            if j % 2 == 0:
                print sub_mo + child_mo[j]
                mo_list.append(sub_mo + child_mo[j])
            else:
                mo_list.append(child_mo[j])

    print mo_list

    b = call_moGet(mo_list)
    print b
    if b == 0:
        l = POINTER(c_char_p * len(mo_list)).in_dll(webapi, 'value')
        print [i for i in l.contents]
    else:
        print "GET failed!!!"


def apply_license(filename):
    ret = webapi.applyLicenseFile(filename)
    print ret
    return ret


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def apply_config(request):
    time.sleep(3)
    return JsonResponse({'30':'30'})
