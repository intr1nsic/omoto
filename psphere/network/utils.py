"""
:mod:`omoto.network.utils` - A utility file for working with subnets
=============================================

.. module:: utils

A module that addresses usage with subnets and vlans

.. moduleauthor:: David Scherer
.. moduleauthor:: intr1nsic <intr1nsic@tallshorts.com>

"""
import iptools
import socket
from psphere.errors import ConfigError

class Subnet(object):
    """
    A subnet class with several helper functions
    
    :param cidr: A network in cidr notation. e.g. 192.168.1.0/24
    :type cidr: str
    :param low_gateway: Use a low gateway. e.g. 192.168.1.1
    :type low_gateway: bool
    
    >>> from omoto.network.utils import Subnet
    >>> network = Subnet('192.168.1.0/24')
    >>> network.getGateway
    '192.168.1.254'
    >>> network = Subnet('192.168.1.0/24', low_gateway=True)
    >>> network.getGateway
    '192.168.1.1'
    
    """
    def __init__(self, cidr, low_gateway=False):
        if not iptools.validate_cidr(cidr):
            raise ConfigError("CIDR must be in proper format. e.g. 192.168.1.0/24")

        self.base, self.msk = cidr.split('/')
        self.mask = int(self.msk)
        self.num_addr = 2**(32-self.mask)
        self.first_address = iptools.ip2long(self.base)
        self.last_address = iptools.ip2long(self.base) + self.num_addr - 1
        self.low_gateway = low_gateway 
        
    @property
    def first(self):
        """ 
        Return the first IP address in the CIDR 
        
        >>> network = Subnet('192.168.1.0/24')
        >>> network.first
        '192.168.1.0'
        """
        return iptools.long2ip(self.first_address)
        
    @property
    def last(self):
        """ 
        Return the last IP address in the CIDR
        
        >>> network = Subnet('192.168.1.0/24')
        >>> network.last
        '192.168.1.255'
        """
        return iptools.long2ip(self.last_address)
    
    def contains(self, ip):
        """
        Check if the IP is in the subnet
        
        >>> network = Subnet('192.168.1.0/24')
        >>> network.contains('192.168.1.1')
        True
        
        :param ip: An IP address
        :type ip: str
        """
        ip = str(ip)
        ip_as_dec = iptools.ip2long(ip)
        if (ip_as_dec >= self.first_address) and (ip_as_dec <= self.last_address):
            return True
        else:
            return False
            
    def usable_addresses(self, low_reserve=5, high_reserve=5):
        """
        Returns a list of the usable IP addresses in the CIDR range
        
        >>> network = Subnet('192.168.1.0/24')
        >>> len(network.usable_addresses())
        244
        
        :param low_reserve: Reserve how many low ip addresses. Default: 5
        :type low_reserve: int
        :param high_reserve: Reserver how many high ip addreses. Default: 5
        :type high_reserve: int
        """
        first_usable = self.first_address + low_reserve
        last_usable = self.last_address - high_reserve

        if self.low_gateway:
            first_usable += 2
        else:
            last_usable -= 1

        total = last_usable - first_usable
        addresses = []
        for i in range(first_usable, last_usable, 1):
            ip = iptools.long2ip(i)
            addresses.append(ip)
        return addresses

    @property
    def getNetmask(self):
        """
        Return the netmask for the CIDR range
        
        >>> network = Subnet('192.168.1.0/24')
        >>> network.getNetmask
        '255.255.255.0'
        """
        decmask = 0
        for i in range(0,31):
            if (i < self.mask):
                decmask += 1*2**(31-i)
        return iptools.long2ip(decmask)
    
    @property
    def getGateway(self):
        """
        Return the gateway address of the CIDR range
        
        >>> network = Subnet('192.168.1.0/24')
        >>> network.getGateway
        '192.168.1.254'
        """
        if self.low_gateway:
            return iptools.long2ip(iptools.ip2long(self.base) + 1)
        else:
            return iptools.long2ip(iptools.ip2long(self.base) + self.num_addr - 2)
                                                                               
class Vlan(Subnet):
    """
    Takes a vlan ID and CIDR range for vlan <-> subnet association
    
    :param id: Vlan ID. e.g. 101
    :type id: int
    :param cidr: Network CIDR notation. e.g. '192.168.1.0/24'
    :type cidr: str
    
    >>> from omoto.network.utils import Vlan
    >>> vlan = Vlan('405', '192.168.1.0/24')
    >>> vlan.first
    '192.168.1.0'
    """
    def __init__(self, id, cidr):
        self.vlanid = id
        Subnet.__init__(self, cidr)

def resolve_hostname(hostname, domain):
    """
    resolve_hostname('google', 'com')
    fqdn = google.com
    'x.x.x.x'
    """
    fqdn = hostname + "." + domain
    try:
        ip = socket.gethostbyname(fqdn)
        ip = str(ip)
        return ip
    except:
        return 0


""" Begin Testing """        
def utils_test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    utils_test()