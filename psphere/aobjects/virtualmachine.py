from psphere import managedobjects
from psphere.errors import TaskFailedError, ActionError

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
		except ActionError, e:
			raise e

	@property
	def get_power_state(self):
		""" Return the power state of the VM """
		self.update()
		return self.summary.runtime.powerState