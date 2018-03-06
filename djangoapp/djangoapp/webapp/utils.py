from djangoapp.settings import PORTCONFIG_PERSISTENCE_FILE  # , webapi
from ctypes import *
import struct
import socket
import enum


class MO_TYPE(enum.Enum):
    STRING = "6",
    INT = "7",
    UINT = "9",
    BOOLEAN = "18",
    DATETIME = "11"


class STATICPort(Structure):
    _fields_ = [("IPAddr", c_uint),
                ("Mask", c_uint),
                ("GW", c_uint),
                ("DNSPri", c_uint),
                ("DNSSec", c_uint),
                ("DhcpEnable", c_uint)]


class INTERFACE(enum.Enum):
    IPSEC = "1"
    MGMT = "2"
    TIMING = "3"
    BC = "4"
    IPSEC2 = "5"
    RDNCY = "6"


def call_moGet(param_list):
    arr = (c_char_p * len(param_list))()
    arr[:] = param_list
    return webapi.moGet(arr, len(param_list))


def call_moSet(param_list):
    arr = (c_char_p * len(param_list))()
    arr[:] = param_list
    return webapi.moSet(arr, len(param_list))


# Extras
def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))


def get_iface_data(iface_no):
    f = open(PORTCONFIG_PERSISTENCE_FILE, "r")
    iface_info = f.readlines()

    iface = STATICPort()
    iface.IPAddr = int(iface_info[iface_no * 6 + 0], 16)
    iface.Mask = int(iface_info[iface_no * 6 + 1], 16)
    iface.GW = int(iface_info[iface_no * 6 + 2], 16)
    iface.DNSPri = int(iface_info[iface_no * 6 + 3], 16)
    iface.DNSSec = int(iface_info[iface_no * 6 + 4], 16)
    iface.DhcpEnable = int(iface_info[iface_no * 6 + 5], 16)

    f.close()
    return iface


def set_iface_data(iface_info):
    ret = webapi.setport(iface_info,1)
    return ret