from psphere import managedobjects
from psphere.errors import TaskFailedError, ActionError
import datetime

class VirtualMachine(managedobjects.VirtualMachine):
	def __init__(self, mo_ref, client):
		managedobjects.VirtualMachine.__init__(self, mo_ref, client)


	def power_on(self, async=True):
		""" 
		Power on a Virtual Machine.
		Allows the option to either return the task
		or wait for the task to finish
		"""
		# Because it may break
		try:
			task = self.PowerOnVM_Task()

			if async:
				status = task.wait_for_state([task.STATE_SUCCESS,
												task.STATE_ERROR])

				if status == task.STATE_ERROR:
					raise TaskFailedError(task.get_error_message)

				# Task completed, update object and return
				self.update()
				return

			# task was sync, return the task
			return task

		# Uh oh, something failed.
		except TaskFailedError, e:
			raise e

	def power_off(self, async=True):
		"""
		Power off a Virtual Machine
		Allows the option to either return the task
		or wait for the task to finish
		"""
		# Because it may break
		try:
			task = self.PowerOffVM_Task()

			if async:
				status = task.wait_for_state([task.STATE_SUCCESS,
												task.STATE_ERROR])

				if status == task.STATE_ERROR:
					raise TaskFailedError(task.get_error_message)

				# Task completed, update object and return
				self.update()
				return

			# Task was sync, return the task
			return task

		# Uh oh, something failed.
		except TaskFailedError, e:
			raise e

	def reset(self, async=True):
		"""
		Reset the Virtual Machine
		Allows the option to either return the task
		or wait for the task to finish
		"""
		# Because it may break
		try:
			task = self.ResetVM_Task()

			if async:
				status = task.wait_for_state([task.STATE_SUCCESS,
												task.STATE_ERROR])

				if status == task.STATE_ERROR:
					raise TaskFailedError(task.get_error_message)

				# Task completed, update object and return
				self.update()
				return

			# Task was sync, return the task
			return task
			
		except TaskFailedError, e:
			raise e

	def reboot_guest(self):
		""" Attempts to reboot the guest """
		try:
			self.RebootGuest()
			self.update()
			return
		except ActionError, e:
			raise e

	def shutdown_guest(self):
		""" Attempts to shutdown the guest """
		try:
			self.ShutdownGuest()
			self.update()
			return
		except ActionError, e:
			raise e

	def standby_guest(self):
		""" Attempts to put the guest in standby """
		try:
			self.StandbyGuest()
			self.update()
			return
		except ActionError, e:
			raise e

	def uptime(self):
		""" Return the VM uptime """
		
		# Get the latest information
		self.update()

		now = datetime.datetime.now()
		bootTime = self.summary.runtime.bootTime
		uptime = now - bootTime
		return str(uptime)

	def get_committed_storage(self):
		""" Return total committed storage """

		# Again, lets get the latest information
		self.update()

		# Some VM's may have many disks, so lets itterate over the list
		# and add them up
		committed = 0
		for disk in self.storage.perDatastoreUsage:
			committed += disk['committed']

		return committed

	def get_uncommitted_storage(self):
		""" Return total uncommitted storage """

		# Update for latest info
		self.update()

		uncommitted = 0
		for disk in self.storage.perDatastoreUsage:
			uncommitted += disk['committed']

		return uncommitted

	def get_unshared_storage(self):
		""" Return total unshared storage """

		# Update for latest info
		self.update()
		shared = 0
		for disk in self.storage.perDatastoreUsage:
			shared += disk['shared']

		return shared

	def get_power_state(self):
		""" Return the power state of the VM """
		self.update()
		if hasattr(self.summary.runtime, "powerState"):
			return self.summary.runtime.powerState
		else:
			return "poweredOff"
			
	def upgrade_tools(self, async=True):
		""" Try to upgrade tools on the VM """
		try:
			task = self.UpgradeTools_Task()

			if async:
				status = task.wait_for_state([task.STATE_SUCCESS,
												task.STATE_ERROR])

				if status == task.STATE_ERROR:
					raise TaskFailedError(task.get_error_message)
					
				# Task completed, update object and return
				self.update()
				return

			# Task was sync, return the task
			return task

		except TaskFailedError, e:
			raise e

	@property
	def is_template(self):
		"""
		Return true if template, else false
		"""
		return self.summary.config.template