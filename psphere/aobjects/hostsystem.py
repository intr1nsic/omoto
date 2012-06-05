from psphere import managedobjects
from psphere.errors import ConfigError, TaskFailedError, ActionError

class HostSystem(managedobjects.HostSystem):
	def __init__(self, mo_ref, client):
		managedobjects.HostSystem.__init__(self, mo_ref, client)
		self.client = client

	def query_cdp_detail(self, raw=False):
		"""
		Takes a host object and returns a dictionary of
		virtual nics and the connected switch and port
		
		"vmnic0": {
			switch: "switch01"
			port: "GigabitEthernet1/2"
			}
		}

		Option to return the raw result of the query
		"""
		# Query our devices for info
		net_hint = self.configManager.networkSystem.QueryNetworkHint()

		if raw:
			return net_hint

		cdp_info = {}

		for neighbor in net_hint:
			if hasattr(neighbor, 'connectedSwitchPort'):
				cdp_info[neighbor.device] = {}

				# Some switches don't return a system name, fall back
				if not neighbor['connectedSwitchPort']['systemName']:
					cdp_info[neighbor.device]['switch'] = \
						neighbor['connectedSwitchPort']['devId']
				else:
					cdp_info[neighbor.device]['switch'] = \
						neighbor['connectedSwitchPort']['systemName']

				cdp_info[neighbor.device]['port'] = \
					neighbor['connectedSwitchPort']['portId']
				cdp_info[neighbor.device]['nvlan'] = \
					neighbor['connectedSwitchPort']['vlan']
			else:
				# Nic not connected to CDP enabled Device
				cdp_info[neighbor.device] = {
												'port': None,
												'switch': None,
												'nvlan': None,
											}

		return cdp_info

	def get_uptime(self):
		"""
		Query the host for system uptime
		returns uptime in seconds
		"""
		uptime = self.RetrieveHardwareUptime()
		return uptime

	def list_vswitches(self):
		"""
		Return a list of names of configured vswitches on the host
		"""
		self.update()

		net_conf = self.configManager.networkSystem.networkConfig['vswitch']

		vswitches = []

		for vswitch in net_conf:
			vswitches.append(vswitch['name'])

		return vswitches

	def add_pg_to_vswitch(self, name=None, vlan=None, vswitch=None):
		"""
		Method to easily add a new portgroup to a vswitch on a host

		:param name: Name of the Port Group. e.g. "Public Network"
		:type name: str
		:param vlan: a vlan ID. e.g. 200
		:type vlan: int
		:param vswitch: Name of the vswitch. Can grab this from list_vswitches()
		:type vswitch: str
		"""

		# Since this is a network group, lets inspect and double inspect
		if not isinstance(name, str):
			raise ConfigError("Portgroup Name must be a str")

		if not isinstance(vlan, int):
			raise ConfigError("vlan must be an integer")

		if not isinstance(vswitch, str):
			raise ConfigError("vswitch must be a str")

		actv_vswitches = self.list_vswitches()

		if vswitch not in actv_vswitches:
			raise ConfigError("Specified vswitch does not exist on the host")

		host_pg_spec = self.client.create("HostPortGroupSpec")

		# Grab our HostNetwork mo_ref
		host_network = self.configManager.networkSystem

		# Build out our HostPortGroupSpec
		host_pg_spec.name = name
		host_pg_spec.vlanId = vlan
		host_pg_spec.vswitchName = vswitch
		
		try:
			self.update()
			host_network.AddPortGroup(portgrp=host_pg_spec)
			
			# Everything worked, return ok
			return 0

		except Exception, e:
			raise ActionError("Unable to add portgroup", e)

	def create_vswitch(self, name=None, mtu=1500, spec=None, numPorts=1024):
		"""
		Create a standard vswitch on the host.

		Default MTU ( 1500 ) will be used
		Default Port Counts will be the max, 1024

		:param name: vSwitch name
		:type name: str
		:param mtu: MTU for the created vSwitch
		:type mtu: int
		:param spec: Custom Spec. Otherwise, a default will be used
		:type spec: HostVirtualSwitchSpec
		:param numPorts: Number of ports to create on the vSwitch
		:type numPorts: int
		"""

		if spec:
			if not hasattr(spec, "dynamicType"):
				raise Exception("Invalid Spec")
			else:
				vswitch_spec = spec
		else:
			vswitch_spec = self.client.create("HostVirtualSwitchSpec")
			# We need to delete attr's we aren't using. 
			delattr(vswitch_spec, "bridge")
			delattr(vswitch_spec, "policy")

		# Set some spec values
		vswitch_spec.mtu = mtu
		vswitch_spec.numPorts = numPorts

		# Lets create that spec
		try:
			host_netMgr = self.configManager.networkSystem
			host_netMgr.AddVirtualSwitch(vswitchName=name, spec=vswitch_spec)
			return
		except Exception, e:
			raise ActionError(e)

	def enable_lockdown(self):
		"""
		Modifies the permision of the host so that it can only be
		accessed through the local console or an authorized centralized
		management application. 
		"""
		try:
			self.EnterLockdownMode()
			self.update()
			return
		except ActionError, e:
			raise e

	def disable_lockdown(self, async=True):
		"""
		Modifies the permision of the host and restores Administrator
		permission for the local administrative account.
		"""
		try:
			self.ExitLockdownMode()
			self.update()
			return
		except ActionError, e:
			raise e
