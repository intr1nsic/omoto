from psphere import managedobjects

class ComputeResource(managedobjects.ComputeResource):
	def __init__(self, mo_ref, client):
		managedobjects.ComputeResource.__init__(self, mo_ref, client)

class ClusterComputeResource(managedobjects.ClusterComputeResource):
	def __init__(self, mo_ref, client):
		managedobjects.ClusterComputeResource.__init__(self, mo_ref, client)

	def add(self, x, y):
		return x + y