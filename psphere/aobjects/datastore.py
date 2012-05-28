from psphere import managedobjects
from psphere.network import utils

class Datastore(managedobjects.Datastore):
	def __init__(self, mo_ref, client):
		managedobjects.Datastore.__init__(self, mo_ref, client)

	@property
	def provisioned_space(self):
		"""
		Return the provisioned space
		"""
		self.provisioned = (self.capacity_space - self.free_space) + \
			self.uncommitted_space
		return self.provisioned

	@property
	def capacity_space(self):
		"""
		Return the capacity of the Datastore
		"""
		return self.summary.capacity

	@property
	def free_space(self):
		"""
		Return the free space of the Datastore
		"""
		return self.summary.freeSpace

	@property
	def used_space(self):
		"""
		Return the used space of the Datastore
		"""
		self.used = self.capacity_space - self.free_space
		return self.used

	@property
	def uncommitted_space(self):
		"""
		Return the uncommitted space
		"""
		try:
			self.uncommitted = self.summary.uncommitted
		except:
			self.uncommitted = 0
		return self.uncommitted

""" Begin Testing """
def datastore_test():
	import doctest
	doctest.testmod()

if __name__ == '__main___':
	datastore_test()