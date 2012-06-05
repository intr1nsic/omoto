from psphere import managedobjects
from psphere.network import utils

import inspect

class Datacenter(managedobjects.Datacenter):
	def __init__(self, mo_ref, client):
		managedobjects.Datacenter.__init__(self, mo_ref, client)
		self.client = client

	def add_vlan(self, vlan, cidr):
		"""
		Add a vlan and network to a Datacenter

		:param vlan: a vlan ID. e.g. 200
		:type vlan: int
		:param cidr: Network in CIDR. e.g. 192.168.1.0/24
		:type cidr: str
		"""
		self.vlans[vlan] = utils.Vlan(vlan, cidr)

	@classmethod
	def create_dc(cls, client, name=None, folder=None):
		"""
		Create a datacenter. Optionally you can include
		a mo_ref to a Folder in which you want to create
		the datacenter

		:param folder: mo_ref to the folder for the datacenter
		:type folder: mo_ref
		"""

		if folder:
			# Test to make sure its a ref
			if not hasattr(folder, "_mo_ref"):
				raise Exception("Folder is not a mo_ref.")
			else:
				rootFolder = folder
		else:
			rootFolder = client.sc.rootFolder

		try:
			dc = rootFolder.CreateDatacenter(name=name)
			return dc
		except Exception, e:
			raise e


		


""" Begin Testing """
def datacenter_test():
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	datacenter_test()