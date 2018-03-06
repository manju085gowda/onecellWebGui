from django import forms
from django.core.validators import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory

# Deployment Questionnaire choices
BC_MME_CHOICES = (
    ('S1', 'Security Gateway1 (S1)'),
    ('NonIPSec', 'Non IPSec Mode'),
)

BC_HEMS_CHOICES = (
    ('S1', 'Security Gateway1 (S1)'),
    ('OAM', 'Security Gateway2 (OAM)'),
    ('NonIPSec', 'Non IPSec Mode'),
)

BC_CA_CHOICES = (
    ('S1', 'Security Gateway1 (S1)'),
    ('OAM', 'Security Gateway2 (OAM)'),
    ('NonIPSec', 'Non IPSec Mode'),
    ('None', 'No CA')
)

BC_TIMING_CHOICES = (
    ('GPS', 'GPS'),
    ('PTP', 'Bounday Clock (BC)'),
)

BC_PTP_PORT_CHOICES = (
    ('BC', 'Using Boundary Clock port'),
    ('BH', 'Using Backhaul Port'),
)

REDUNDANCY_ENABLE_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

INTERFACE_MODE_CHOICES = (
    ('static', 'Static'),
    ('dhcp', 'DHCP'),
)

ADDRESS_TYPE_CHOICES = (
    ('Static', 'Static'),
    ('Dynamic', 'Dynamic'),
)

EXCLUDE_CP_CHOICES = (
    ('TRUE', 'True'),
    ('FALSE', 'False'),
)

HEMS_ACCESS_CHOICES = (
    ('IPSec', 'IPSec'),
    ('NonIPSec', 'Non IPSec'),
)

CA_SERVER_ACCESS_CHOICES = (
    ('IPSec', 'IPSec'),
    ('NonIPSec', 'Non IPSec'),
)

NON_IPSEC_HTTPS_CHOICES = (
    ('TRUE', 'Yes'),
    ('FALSE', 'No'),
)

SNMP_FEATURE_CHOICES = (
    ('Enable', 'Enable'),
    ('Disable', 'Disable'),
)

AUTH_PROTOCOL_CHOICES = (
    ('HMAC-MD5-96', 'HMAC-MD5-96'),
    ('HMAC-SHA-96', 'HMAC-SHA-96'),
)

PRIVATE_PROTOCOL_CHOICES = (
    ('NONE', 'NONE'),
    ('CBC-DES', 'CBC-DES'),
)

REDUNDANCY_FEATURE_CHOICES = (
    ('Enable', 'Enable'),
    ('Disable', 'Disable'),
)

REDUNDANCY_BC_STATE_CHOICES = (
    ('Standby', 'Standby'),
    ('Active', 'Active'),
)

TIMING_MODE_CHOICES = (
    ('GPS', 'GPS'),
    ('PTP', 'PTP'),
)

LATITUDE_SIGN_CHOICES = (
    ('North', 'North'),
    ('South', 'South'),
)

DIRECTION_OF_ALTITUDE_CHOICES = (
    ('Height', 'Height'),
    ('Depth', 'Depth'),
)

LANGUAGE = (
    ('en-us', 'English-US'),
    ('german', 'German'),
    ('en-uk', 'English-UK'),
)

ip_address_errors = {
    'required': 'IP address cannot be empty',
    'invalid': 'Invalid IP address'
}
subnet_errors = {
    'required': 'Subnet cannot be empty',
    'invalid': 'Invalid subnet. Subnet mask must be between 1 and 32'
}
default_gateway_errors = {
    'required': 'Default Gateway IP address cannot be empty',
    'invalid': 'Invalid Gateway IP address'
}
primary_dns_errors = {
    'required': 'Primary DNS address cannot be empty',
    'invalid': 'Invalid Primary DNS address',
}
secondary_dns_errors = {
    'invalid': 'Invalid Secondary DNS address'
}

vlan_id_errors = {
    'required': 'VLAN ID cannot be empty',
    'invalid': 'Invalid VLAN ID. Enter a value between 11 and 4095'
}
mtu_errors = {
    'required': 'MTU cannot be empty',
    'invalid': 'Invalid MTU. Enter a value between 68 and 1998'
}

secgw_errors = {
    'required': 'Security Gateway cannot be empty',
    'invalid': 'Invalid Security Gateway'
}
internal_address_errors = {
    'required': 'Internal Address cannot be empty',
    'invalid': 'Invalid Internal Address'
}
internal_netmask_errors = {
    'invalid': 'Invalid Netmask'
}
internal_dns_errors = {
    'invalid': 'Invalid Internal DNS'
}

ptp_server_errors = {
    'required': 'PTP servers cannot be empty',
    'invalid': 'Invalid PTP servers'
}
degrees_latitude_errors = {
    'required': 'Degrees of Latitude cannot be empty',
}
degrees_longitude_errors = {
    'required': 'Degrees of Longitude cannot be empty',
}
altitude_errors = {
    'required': 'Altitude cannot be empty',
}
uncertainity_semimajor_errors = {
    'required': 'Uncertainity Semimajor cannot be empty',
}
uncertainity_semiminor_errors = {
    'required': 'Uncertainity Semiminor cannot be empty',
}
uncertainity_altitude_errors = {
    'required': 'Uncertainity Altitude cannot be empty',
}
orientation_majoraxis_errors = {
    'required': 'Orientation of Major axis cannot be empty',
}
confidence_errors = {
    'required': 'Confidence cannot be empty',
}

bcid_errors = {
    'required': 'BCID cannot be empty',
    'invalid': 'Invalid BCID. Enter a value between 1 and 255'
}
iq_vlanid_errors = {
    'required': 'VLAN ID cannot be empty',
    'invalid': 'Invalid VLAN ID. Enter a value between 1 and 4094'
}
tcid_errors = {
    'required': 'TCID cannot be empty',
    'invalid': 'Invalid TCID. Enter a value between 1 and 255'
}

vcid_errors = {
    'required': 'Virtual Cell ID cannot be empty',
    'invalid': 'Invalid Virtual Cell ID'
}

hems_url_errors = {
    'required': 'HeMS URL cannot be empty',
    'invalid': 'Invalid HeMS URL',
}

caserver_ip_errors = {
    'required': 'CA Server cannot be empty',
    'invalid': 'Invalid CA Server'
}
caserver_id_errors = {
    'required': 'CA Server Identity cannot be empty',
    'invalid': 'Invalid CA Server Identity'
}
caserver_uri_errors = {
    'required': 'CA Server URI cannot be empty',
    'invalid': 'Invalid CA Server URI'
}
caserver_port_errors = {
    'required': 'CA Server Port cannot be empty',
    'invalid': 'Invalid CA Server Port. Enter a value between 1 and 65535'
}
sacert_id_errors = {
    'invalid': 'Invalid SA Certificate Identifier'
}
pki_message_errors = {
    'invalid': 'Invalid PKI Message Hash'
}

snmp_ip_errors = {
    'required': 'SNMP IP cannot be empty',
    'invalid': 'Invalid SNMP IP'
}
snmp_port_errors = {
    'required': 'SNMP Port cannot be empty',
    'invalid': 'Invalid SNMP Port'
}
username_errors = {
    'required': 'Username cannot be empty',
    'invalid': 'Invalid username'
}
authkey_errors = {
    'required': 'Auth Key cannot be empty',
    'invalid': 'Invalid Auth Key'
}
privatekey_errors = {
    'required': 'Private Key cannot be empty',
    'invalid': 'Invalid Private Key'
}


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    language = forms.ChoiceField(widget=forms.Select(attrs={'class': ' dropdown-toggle  form-control'}),choices=LANGUAGE, label='',required=False)


class DeploymentQuestionnaireForm(forms.Form):
    bc_mme_communication = forms.ChoiceField(choices=BC_MME_CHOICES, widget=forms.RadioSelect(), initial='NonIPSec')
    bc_hems_communication = forms.ChoiceField(choices=BC_HEMS_CHOICES, widget=forms.RadioSelect(), initial='NonIPSec')
    bc_ca_communication = forms.ChoiceField(choices=BC_CA_CHOICES, widget=forms.RadioSelect(), initial='None')
    bc_timing = forms.ChoiceField(choices=BC_TIMING_CHOICES, widget=forms.RadioSelect(), initial='GPS')
    bc_ptp_port = forms.ChoiceField(choices=BC_PTP_PORT_CHOICES, widget=forms.RadioSelect(), initial='BC')
    bc_redundancy_enable = forms.ChoiceField(choices=REDUNDANCY_ENABLE_CHOICES, widget=forms.RadioSelect(),
                                             initial='No')


# Form class for File Upload
class ConfigFileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'style': 'display:none;'}), label="")


class IpAddressForm(forms.Form):
    Mode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'mutator'}), choices=INTERFACE_MODE_CHOICES, initial='dhcp')
    IPAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid IP Address'}),
        error_messages=ip_address_errors)
    SubnetMask = forms.IntegerField(min_value=1, max_value=32, label="Subnet", widget=forms.TextInput(
        attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 32'}), error_messages=subnet_errors)
    DefaultGateway = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid gateway Address'}),
        error_messages=default_gateway_errors)
    PrimaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid Primary DNS Address'}),
        error_messages=primary_dns_errors)
    SecondaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid Secondary DNS Address'}),
        error_messages=secondary_dns_errors, required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(IpAddressForm, self).__init__(data, *args, **kwargs)
        print data
        print data.get('Mode')
        # dhcp
        if data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[1][0]:
            self.fields['IPAddress'].required = False
            self.fields['SubnetMask'].required = False
            self.fields['DefaultGateway'].required = False
            self.fields['PrimaryDNSAddress'].required = False
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required
        # static
        elif data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[0][0]:
            self.fields['IPAddress'].required = True
            self.fields['SubnetMask'].required = True
            self.fields['DefaultGateway'].required = True
            self.fields['PrimaryDNSAddress'].required = True
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required


class MgmtPortConfigForm(IpAddressForm):
    pass


# Form class for SecGW configuration
class S1ConfigForm(forms.Form):
    VLANID = forms.IntegerField(min_value=11, max_value=4095,
                                widget=forms.TextInput(
                                    attrs={'class': 'inputboxbig', 'title': 'Enter a value between 11 and 4095','id':'s1_vlanid'}),
                                error_messages=vlan_id_errors)
    MTU = forms.IntegerField(min_value=64, max_value=1998,
                             widget=forms.TextInput(
                                 attrs={'class': 'inputboxbig', 'title': 'Enter a value between 68 and 1998'}),
                             error_messages=mtu_errors)
    Mode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 's1_mode','class': 'mutator'}), choices=INTERFACE_MODE_CHOICES,
                             initial='dhcp')
    IPAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid IP Address', 'id': 's1_ip'}),
        error_messages=ip_address_errors)
    SubnetMask = forms.IntegerField(min_value=1, max_value=32, widget=forms.TextInput(
        attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 32', 'id': 's1_subnet'}),
                                    error_messages=subnet_errors)
    DefaultGateway = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid gateway Address', 'id': 's1_gateway'}),
        error_messages=default_gateway_errors)
    PrimaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid Primary DNS Address', 'id': 's1_pdns'}),
        error_messages=primary_dns_errors)
    SecondaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid Secondary DNS Address', 'id': 's1_sdns'}),
        error_messages=secondary_dns_errors, required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(S1ConfigForm, self).__init__(data, *args, **kwargs)
        print "S1ConfigForm"
        print data
        print data.get('Mode')
        # dhcp
        if data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[1][0]:
            self.fields['IPAddress'].required = False
            self.fields['SubnetMask'].required = False
            self.fields['DefaultGateway'].required = False
            self.fields['PrimaryDNSAddress'].required = False
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required
        # static
        elif data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[0][0]:
            self.fields['IPAddress'].required = True
            self.fields['SubnetMask'].required = True
            self.fields['DefaultGateway'].required = True
            self.fields['PrimaryDNSAddress'].required = True
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required


class SecGW1Form(forms.Form):
    SecGWURL = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'SecGW1URL'}), required=True,
                              error_messages=secgw_errors)
    AddressType = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle inputboxbig mutator','id':'SecGW1AddressType'}),
                                    choices=ADDRESS_TYPE_CHOICES)
    InternalAddress = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'SecGW1-InternalAddress'}),
                                     error_messages=internal_address_errors)
    #InternalNetMask = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'secgw1_in'}),
    #                                 error_messages=internal_netmask_errors)
    InternalNetMask = forms.IntegerField(min_value=1, max_value=32, widget=forms.TextInput(attrs={'class': 'inputboxbig', 'id': 'SecGW1-InternalNetMask'}),
                             error_messages=internal_netmask_errors)
    InternalDNS = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'SecGW1-InternalDNS'}),
                                 error_messages=internal_dns_errors)
    #InternalDHCP = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'SecGW1-InternalDHCP'}))
    ExcludeCP = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig','id':'SecGW1-ExcludeCP'}),
                                  choices=EXCLUDE_CP_CHOICES, initial='False')

    def __init__(self, data=None, *args, **kwargs):
        super(SecGW1Form, self).__init__(data, *args, **kwargs)
        print "SecGW1Form"
        print data
        print data.get('AddressType')
        # Dynamic
        if data and data.get('AddressType', None) == ADDRESS_TYPE_CHOICES[1][0]:
            self.fields['InternalAddress'].required = False
            self.fields['InternalNetMask'].required = False
            self.fields['InternalDNS'].required = False
            #self.fields['InternalDHCP'].required = False
            print self.fields['InternalAddress'].required
        # Static
        elif data and data.get('Mode', None) == ADDRESS_TYPE_CHOICES[0][0]:
            self.fields['InternalAddress'].required = True
            self.fields['InternalNetMask'].required = True
            self.fields['InternalDNS'].required = True
            #self.fields['InternalDHCP'].required = True
            print self.fields['InternalAddress'].required


class OAMConfigForm(forms.Form):
    VLANID = forms.IntegerField(min_value=11, max_value=4095,
                                widget=forms.TextInput(attrs={'class': 'inputboxbig', 'id': 'oam_vlanid',
                                                              'title': 'Enter a value between 11 and 4095'}),
                                error_messages=vlan_id_errors)
    MTU = forms.IntegerField(min_value=64, max_value=1998,
                             widget=forms.TextInput(attrs={'class': 'inputboxbig', 'id': 'oam_mtu',
                                                           'title': 'Enter a value between 68 and 1998'}),
                             error_messages=mtu_errors)
    Mode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'oam_mode','class': 'mutator'}), choices=INTERFACE_MODE_CHOICES,
                             initial='dhcp')
    IPAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid IP Address', 'id': 'oam_ip'}),
        error_messages=ip_address_errors)
    SubnetMask = forms.IntegerField(min_value=1, max_value=32, widget=forms.TextInput(
        attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 32', 'id': 'oam_subnet'}),
                                    error_messages=subnet_errors)
    DefaultGateway = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid gateway Address', 'id': 'oam_gateway'}),
        error_messages=default_gateway_errors)
    PrimaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid Primary DNS Address', 'id': 'oam_pdns'}),
        error_messages=primary_dns_errors)
    SecondaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid Secondary DNS Address', 'id': 'oam_sdns'}),
        error_messages=secondary_dns_errors, required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(OAMConfigForm, self).__init__(data, *args, **kwargs)
        print "OAMConfigForm"
        print data
        print data.get('Mode')
        # dhcp
        if data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[1][0]:
            self.fields['IPAddress'].required = False
            self.fields['SubnetMask'].required = False
            self.fields['DefaultGateway'].required = False
            self.fields['PrimaryDNSAddress'].required = False
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required
        # static
        elif data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[0][0]:
            self.fields['IPAddress'].required = True
            self.fields['SubnetMask'].required = True
            self.fields['DefaultGateway'].required = True
            self.fields['PrimaryDNSAddress'].required = True
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required


class SecGW2Form(forms.Form):
    SecGWURL = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'SecGW2URL'}), required=True,
                              error_messages=secgw_errors)
    AddressType = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle inputboxbig mutator','id':'SecGW2AddressType'}),
                                    choices=ADDRESS_TYPE_CHOICES, initial='Dynamic')
    InternalAddress = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'SecGW2-InternalAddress'}),
                                     error_messages=internal_address_errors)
    # InternalNetMask = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'secgw1_in'}),
    #                                 error_messages=internal_netmask_errors)
    InternalNetMask = forms.IntegerField(min_value=1, max_value=32,
                                         widget=forms.TextInput(attrs={'class': 'inputboxbig', 'id': 'SecGW2-InternalNetMask'}),
                                         error_messages=internal_netmask_errors)
    InternalDNS = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig', 'id': 'SecGW2-InternalDNS'}),
                                 error_messages=internal_dns_errors)
    # InternalDHCP = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','id':'secgw1_idhcp'}))
    ExcludeCP = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig', 'id': 'SecGW2-ExcludeCP'}),
        choices=EXCLUDE_CP_CHOICES, initial='False')

    def __init__(self, data=None, *args, **kwargs):
        super(SecGW2Form, self).__init__(data, *args, **kwargs)
        print "SecGW2Form"
        print data
        print data.get('AddressType')
        # Dynamic
        if data and data.get('AddressType', None) == ADDRESS_TYPE_CHOICES[1][0]:
            self.fields['InternalAddress'].required = False
            self.fields['InternalNetMask'].required = False
            self.fields['InternalDNS'].required = False
            #self.fields['InternalDHCP'].required = False
            print self.fields['InternalAddress'].required
        # Static
        elif data and data.get('Mode', None) == ADDRESS_TYPE_CHOICES[0][0]:
            self.fields['InternalAddress'].required = True
            self.fields['InternalNetMask'].required = True
            self.fields['InternalDNS'].required = True
            #self.fields['InternalDHCP'].required = True
            print self.fields['InternalAddress'].required


class BCConfigForm(forms.Form):
    # VLANID = forms.IntegerField(min_value=11, max_value=4095,
    #                             widget=forms.TextInput(attrs={'class': 'inputboxbig', 'id': 'bc_vlanid',
    #                                                           'title': 'Enter a value between 11 and 4095'}),
    #                             error_messages=vlan_id_errors)
    # MTU = forms.IntegerField(min_value=64, max_value=1998,
    #                          widget=forms.TextInput(
    #                              attrs={'class': 'inputboxbig', 'id': 'bc_mtu',
    #                                     'title': 'Enter a value between 68 and 1998'}), error_messages=mtu_errors)
    #TimingSource = forms.ChoiceField(widget=forms.RadioSelect, choices=TIMING_MODE_CHOICES, initial='GPS')
    PTPServers = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter IP addresses separated by commas'}),
        validators=[RegexValidator(
            '((25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)(,\n|,?$))',
            message='Ensure IPs are comma seperated')], error_messages=ptp_server_errors)
    Mode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'bc_mode','class': 'mutator'}), choices=INTERFACE_MODE_CHOICES,
                             initial='dhcp')
    IPAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid IP Address', 'id': 'bc_ip'}),
        error_messages=ip_address_errors)
    SubnetMask = forms.IntegerField(min_value=1, max_value=32, widget=forms.TextInput(
        attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 32', 'id': 'bc_subnet'}),
                                    error_messages=subnet_errors)
    DefaultGateway = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid gateway Address', 'id': 'bc_gateway'}),
        error_messages=default_gateway_errors)
    PrimaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid Primary DNS Address', 'id': 'bc_pdns'}),
        error_messages=primary_dns_errors)
    SecondaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid Secondary DNS Address', 'id': 'bc_sdns'}),
        error_messages=secondary_dns_errors, required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(BCConfigForm, self).__init__(data, *args, **kwargs)
        print "BCConfigForm"
        print data
        print data.get('Mode')
        # dhcp
        if data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[1][0]:
            self.fields['IPAddress'].required = False
            self.fields['SubnetMask'].required = False
            self.fields['DefaultGateway'].required = False
            self.fields['PrimaryDNSAddress'].required = False
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required
        # static
        elif data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[0][0]:
            self.fields['IPAddress'].required = True
            self.fields['SubnetMask'].required = True
            self.fields['DefaultGateway'].required = True
            self.fields['PrimaryDNSAddress'].required = True
            self.fields['SecondaryDNSAddress'].required = False
            print self.fields['IPAddress'].required


# Form class for Nominal GPS configuration
class NominalGPSConfigForm(forms.Form):
    LatitudeSign = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),
                                     choices=LATITUDE_SIGN_CHOICES, initial='North')
    DegreesOfLatitude = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 2^23-1'}),
        error_messages=degrees_latitude_errors,
        min_value=0,
        max_value=(2 ** 23) - 1)
    DegreesOfLongitude = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between -2^23-1 and 2^23-1'}),
        error_messages=degrees_longitude_errors,
        min_value=-(2 ** 23) - 1, max_value=(2 ** 23) - 1)
    DirectionOfAltitude = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),
                                            choices=DIRECTION_OF_ALTITUDE_CHOICES, initial='North')
    Altitude = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 2^15-1'}),
        error_messages=altitude_errors,
        min_value=0,
        max_value=(2 ** 15) - 1)
    UncertaintySemiMajor = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 127'}), min_value=0,
        max_value=127, error_messages=uncertainity_semimajor_errors)
    UncertaintySemiMinor = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 127'}), min_value=0,
        max_value=127,error_messages=uncertainity_semiminor_errors)
    UncertaintyAltitude = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 127'}), min_value=0,
        max_value=127,error_messages=uncertainity_altitude_errors)
    OrientationOfMajorAxis = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 179'}), min_value=0,
        max_value=179,error_messages=orientation_majoraxis_errors)
    Confidence = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a value between 0 and 100'}), min_value=0,
        max_value=100,error_messages=confidence_errors)


class FrontHaulConfigForm(forms.Form):
    BCID = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 255'}), min_value=1,
        max_value=255,error_messages=bcid_errors)
    VLANID = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 4094','id':'fronthaul_vlanid'}), min_value=1,
        max_value=4094,error_messages=iq_vlanid_errors)
    TCID = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 255'}), min_value=1,
        max_value=255, error_messages=tcid_errors)


class RedundancyForm(forms.Form):
    BCRedundancy = forms.BooleanField(widget=forms.CheckboxInput(attrs={'data-toggle': 'toggle', 'data-on': 'Enabled', 'data-off': 'Disabled','class': 'mutator'}))
    CUState = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-btn mutator'}),
                                choices=REDUNDANCY_BC_STATE_CHOICES)
    VirtualCellID = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid Virtual Cell ID'}), validators=[
        RegexValidator('^[A-Za-z][A-Za-z0-9]*$', message="Cannot start with a number")], error_messages=vcid_errors)
    Mode = forms.ChoiceField(widget=forms.RadioSelect(attrs={'id': 'rdncy_mode','class': 'mutator'}), choices=INTERFACE_MODE_CHOICES,
                             initial='dhcp')
    IPAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid IP Address', 'id': 'rdncy_ip'}),
        error_messages=ip_address_errors)
    SubnetMask = forms.IntegerField(min_value=1, max_value=32, widget=forms.TextInput(
        attrs={'class': 'inputbox', 'title': 'Enter a value between 1 and 32', 'id': 'rdncy_subnet'}),
                                    error_messages=subnet_errors)
    DefaultGateway = forms.GenericIPAddressField(
        widget=forms.TextInput(
            attrs={'class': 'inputboxbig', 'title': 'Enter a valid gateway Address', 'id': 'rdncy_gateway'}),
        error_messages=default_gateway_errors)
    PrimaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid Primary DNS Address', 'id': 'rdncy_pdns'}),
        error_messages=primary_dns_errors)
    SecondaryDNSAddress = forms.GenericIPAddressField(
        widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid Secondary DNS Address', 'id': 'rdncy_sdns'}),
        error_messages=secondary_dns_errors, required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(RedundancyForm, self).__init__(data, *args, **kwargs)
        #print "RedundancyForm"
        #print data
        #print data.get('BCRedundancy')
        #print data.get('CUState')
        # Feature Disable
        #if data and data.get('BCRedundancy', None) == REDUNDANCY_FEATURE_CHOICES[1][0]:
        if data and data.get('BCRedundancy', None) == None:
            self.fields['BCRedundancy'].required = False
            self.fields['CUState'].required = False
            self.fields['VirtualCellID'].required = False
            self.fields['Mode'].required = False
            self.fields['IPAddress'].required = False
            self.fields['SubnetMask'].required = False
            self.fields['DefaultGateway'].required = False
            self.fields['PrimaryDNSAddress'].required = False
            self.fields['SecondaryDNSAddress'].required = False
            print "Disabled"
        # Feature Enable
        #elif data and data.get('Mode', None) == REDUNDANCY_FEATURE_CHOICES[0][0]:
        elif data and data.get('BCRedundancy', None) == "on":
            print "Enabled"
            self.fields['CUState'].required = True
            # Standby state
            if data and data.get('CUState', None) == REDUNDANCY_BC_STATE_CHOICES[0][0]:
                self.fields['VirtualCellID'].required = False
                print "1Standby"
            # Active state
            elif data and data.get('CUState', None) == REDUNDANCY_BC_STATE_CHOICES[1][0]:
                self.fields['VirtualCellID'].required = True
                print "1Active"
            self.fields['Mode'].required = True
            # dhcp
            if data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[1][0]:
                self.fields['IPAddress'].required = False
                self.fields['SubnetMask'].required = False
                self.fields['DefaultGateway'].required = False
                self.fields['PrimaryDNSAddress'].required = False
                self.fields['SecondaryDNSAddress'].required = False
            # static
            elif data and data.get('Mode', None) == INTERFACE_MODE_CHOICES[0][0]:
                self.fields['IPAddress'].required = True
                self.fields['SubnetMask'].required = True
                self.fields['DefaultGateway'].required = True
                self.fields['PrimaryDNSAddress'].required = True
                self.fields['SecondaryDNSAddress'].required = False


# Form class for HeMS Configuration
class HeMSConfigForm(forms.Form):
    HeMSURL = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid URL'}),
                             error_messages=hems_url_errors)
    HeMSAccess = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),
                                   choices=HEMS_ACCESS_CHOICES,required=False,disabled=True)


# Form class for CA Server Configuration
class CAServerConfigForm(forms.Form):
    CAServer = forms.URLField(widget=forms.TextInput(attrs={'class': 'inputboxbig','title': 'Enter a valid URL'}),error_messages=caserver_ip_errors)
    CAServerIdentity = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','title': 'Enter a valid URL'}),error_messages=caserver_id_errors)
    CAServerURI = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','title': 'Enter a valid URL'}),error_messages=caserver_uri_errors)
    CAServerPort = forms.IntegerField(min_value=1, max_value=65535,
                                      widget=forms.TextInput(attrs={'class': 'inputboxbig','title': 'Enter a value between 1 and 65535'}),error_messages=caserver_port_errors)
    CAServerAccess = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),
                                       choices=CA_SERVER_ACCESS_CHOICES, disabled=True, required=False)
    NONIPSecHttps = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),
                                      choices=NON_IPSEC_HTTPS_CHOICES)
    SACertificateIdentifier = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','title': 'Enter a valid SA Certificate Identifier'}),error_messages=sacert_id_errors,required=False)
    PKIMessageHash = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig', 'title': 'Enter a valid PKI Message Hash'}),error_messages=pki_message_errors,required=False)


# Form class for SNMP Configuration
class SNMPConfigForm(forms.Form):
    SNMPTraps = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'data-toggle': 'toggle', 'data-on': 'Enable', 'data-off': 'Disable','class': 'mutator'}),required=False)
    SNMPIP = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','title':'Enter a valid IP address'}),error_messages=snmp_ip_errors)
    SNMPPort = forms.IntegerField(min_value=0, max_value=65000, widget=forms.TextInput(attrs={'class': 'inputboxbig','title':'Enter a value between 0 and 65000'}),error_messages=snmp_port_errors)
    USM = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'mutator'}),required=False)
    UserName = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputboxbig','title':'Enter a user name'}),error_messages=username_errors)
    AuthProtocol = forms.ChoiceField(choices=AUTH_PROTOCOL_CHOICES,
                                     widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),required=False)
    AuthKey = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'inputboxbig','title':'Enter the Auth Key'}),error_messages=authkey_errors)
    PrivateProtocol = forms.ChoiceField(choices=PRIVATE_PROTOCOL_CHOICES,
                                        widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),required=False)
    PrivateKey = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'class': 'inputboxbig', 'title':'Enter the Private Key'}),error_messages=privatekey_errors)

    def __init__(self, data=None, *args, **kwargs):
        super(SNMPConfigForm, self).__init__(data, *args, **kwargs)
        print "SNMPConfigForm"
        #print data
        print data.get('SNMPTraps')
        print data.get('USM')
        # disable
        if data and data.get('SNMPTraps', None) == None:
            self.fields['SNMPTraps'].required = False
            self.fields['SNMPIP'].required = False
            self.fields['SNMPPort'].required = False
            self.fields['USM'].required = False
            self.fields['UserName'].required = False
            self.fields['AuthProtocol'].required = False
            self.fields['AuthKey'].required = False
            self.fields['PrivateProtocol'].required = False
            self.fields['PrivateKey'].required = False
        # enable
        elif data and data.get('SNMPTraps', None) == "on":
            self.fields['SNMPIP'].required = True
            self.fields['SNMPPort'].required = True
            self.fields['USM'].required = False
            #if data and data.get('USM', None) == "No":
            if data and data.get('USM', None) == None:
                self.fields['UserName'].required = False
                self.fields['AuthProtocol'].required = False
                self.fields['AuthKey'].required = False
                self.fields['PrivateProtocol'].required = False
                self.fields['PrivateKey'].required = False
            #elif data and data.get('USM', None) == "Yes":
            elif data and data.get('USM', None) == "on":
                self.fields['UserName'].required = True
                self.fields['AuthProtocol'].required = True
                self.fields['AuthKey'].required = True
                self.fields['PrivateProtocol'].required = True
                self.fields['PrivateKey'].required = True


# Form class for Whitelist Configuration
class WhitelistForm(forms.Form):
    whitelist_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'style': 'display:none;'}), label="")
    # whitelist_edit = forms.CharField() # Need to dynamically create this table


# Form class for License Configuration
class LicenseForm(forms.Form):
    license_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'style': 'display:none;'}), label="")


class PreWizard(forms.Form):
    language = forms.ChoiceField(widget=forms.Select(attrs={'class': 'btn dropdown-toggle  inputboxbig'}),
                                 choices=LANGUAGE, label='')



#backhaul_formset = formset_factory(S1ConfigForm,SecGW1Form,OAMConfigForm,SecGW2Form)