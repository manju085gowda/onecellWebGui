# XML tags
ONECELL_PROFILE_XML_STRING = "OneCell-Config-Profile"
PORT_CONFIG_XML_STRING = "Port-Configuration"
MANAGEMENT_INTERFACE_XML_STRING = "Management-Interface-Configuration"
S1_CONFIG_XML_STRING = "S1-Configuration"
OAM_CONFIG_XML_STRING = "OAM-Configuration"
SECGW1_CONFIG_XML_STRING = "SeGW1"
SECGW2_CONFIG_XML_STRING = "SeGW2"
BOUNDARY_CLOCK_CONFIG_XML_STRING = "Boundary-Clock-Configuration"
TIMING_SOURCE_XML_STRING = "TimingSource"
NOMINAL_GPS_CONFIG_XML_STRING = "Nominal-GPS-Configuration"
FRONTHAUL_CONFIG_XML_STRING = "Front-Haul-Configuration"
REDUNDANCY_CONFIG_XML_STRING = "Redundancy"
OPERATOR_CONFIG_XML_STRING = "Operator-Configuration"
HEMS_CONFIG_XML_STRING = "HemsConfig"
CA_SERVER_CONFIG_XML_STRING = "CAServerConfig"
SNMP_CONFIG_XML_STRING = "SNMP-Configuration"
USER_CONFIG_XML_STRING = "User-Configuration"
AUTH_TYPE_XML_STRING = "AuthenticationType"
LDAP_AUTH_XML_STRING = "LDAP-Authentication"
RADIUS_AUTH_XML_STRING = "RADIUS-Authentication"
WHITELIST_CONFIG_XML_STRING = "Whitelist-Configuration"
WHITELIST_STRING = "Whitelist"
ADDITIONAL_FILENAMES_XML_STRING = "Additional-FileNames-Included"
ADDRESS_TYPE_XML_STRING = "AddressType"
INTERNAL_ADDRESS_XML_STRING = "InternalAddress"
INTERNAL_NETMASK_XML_STRING = "InternalNetMask"
INTERNAL_DNS_XML_STRING = "InternalDNS"
EXCLUDE_CP_XML_STRING = "ExcludeCP"

IPADDRESS_XML_STRING = "IPAddress"
SUBNETMASK_XML_STRING = "SubnetMask"
DEFAULTGW_XML_STRING = "DefaultGateway"
PRIDNS_XML_STRING = "PrimaryDNSAddress"
SECDNS_XML_STRING = "SecondaryDNSAddress"
IFACE_MODE_XML_STRING = "Mode"

SECGWURL_XML_STRING = "SecGWURL"
PTPSERVERS_XML_STRING = "PTPServers"

LATITUDESIGN_XML_STRING = "LatitudeSign"
DEGREESOFLATITUDE_XML_STRING = "DegreesOfLatitude"
DEGREESOFLONGITUDE_XML_STRING = "DegreesOfLongitude"
DIRECTIONOFALTITUDE_XML_STRING = "DirectionOfAltitude"
ALTITUDE_XML_STRING = "Altitude"
UNCERTAINITYSEMIMAJOR_XML_STRING = "UncertaintySemiMajor"
UNCERTAINITYSEMIMINOR_XML_STRING = "UncertaintySemiMinor"
UNCERTAINITYALTITUDE_XML_STRING = "UncertaintyAltitude"
ORIENTATIONMAJOR_XML_STRING = "OrientationOfMajorAxis"
CONFIDENCE_XML_STRING = "Confidence"

BCID_XML_STRING = "BCID"
VLANID_XML_STRING = "VLANID"

CUSTATE_XML_STRING = "CUState"
VCID_XML_STRING = "VirtualCellID"
BCREDUNDANCY_XML_STRING = "BCRedundancy"

# Global parsed dict
global parsed_dict
global dq_response_dict

global portconfig_dict #
global mgmt_dict
global s1config_dict
global secgw1_dict
global oamconfig_dict
global secgw2_dict
global bc_dict
global ngps_dict
global fh_dict
global rdncy_dict

global operatorconfig_dict #
global hems_dict
global caserver_dict
global snmp_dict

global user_config_dict
global whitelist_config_dict
global additional_file_dict


# Initialize all dictionary
parsed_dict = {}
hems_dict = {}
dq_response_dict = {'bc_ca_communication': u'NonIPSec',
                    'bc_timing': u'GPS',
                    'bc_redundancy_enable': u'No',
                    'bc_mme_communication': u'NonIPSec',
                    'bc_hems_communication': u'NonIPSec',
                    'bc_ptp_port': u'BC'}

root_cert_dict = {'SerialNo': 'NA',
                  'Issuer': 'NA',
                  'Subject': 'NA',
                  'ValidFrom': 'NA',
                  'ValidTo': 'NA',
                  'Validity': 'NA'}


