from psphere import managedobjects

class HostSystem(managedobjects.HostSystem):
	def __init__(self, mo_ref, client):
		managedobjects.HostSystem.__init__(self, mo_ref, client)


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
				cdp_info[neighbor.device] = None

		return cdp_info

	def get_uptime(self):
		"""
		Query the host for system uptime
		returns uptime in seconds
		"""
		uptime = self.RetrieveHardwareUptime()
		return uptime