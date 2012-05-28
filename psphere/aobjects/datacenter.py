from psphere import managedobjects
from psphere.network import utils

class Datacenter(managedobjects.Datacenter):
	def __init__(self, mo_ref, client):
		managedobjects.Datacenter.__init__(self, mo_ref, client)

	def add_vlan(self, vlan, cidr):
		"""
		Add a vlan and network to a Datacenter

		:param vlan: a vlan ID. e.g. 200
		:type vlan: int
		:param cidr: Network in CIDR. e.g. 192.168.1.0/24
		:type cidr: str
		"""
		self.vlans[vlan] = utils.Vlan(vlan, cidr)

""" Begin Testing """
def datacenter_test():
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	datacenter_test()