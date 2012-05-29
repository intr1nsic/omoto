from psphere import managedobjects
from psphere.errors import TaskFailedError
import time

class Task(managedobjects.Task):

	STATE_ERROR   = 'error'
	STATE_QUEUED  = 'queued'
	STATE_RUNNING = 'running'
	STATE_SUCCESS = 'success'
	
	def __init__(self, mo_ref, client):
		managedobjects.Task.__init__(self, mo_ref, client)

	@property
	def get_info(self):
		""" Return task info in raw format """
		self.update()
		return self.info

	@property
	def get_state(self):
		""" Return the current state of the task """
		self.update()
		if hasattr(self.info, "state"):
			return self.info.state

	def wait_for_state(self, states, check_interval=2, timeout=-1):
		""" Wait for given state """
		if not isinstance(states, list):
			states = [states]

		start_time = time.time()

		while True:
			cur_state = self.get_state
			if cur_state in states:
				return cur_state

			if timeout > 0:
				if (time.time() - start_time) > timeout:
					raise TaskFailedError("Timed out waiting for Task")

			self.update()
			time.sleep(check_interval)

	@property
	def get_error_message(self):
		""" If error exists, return error message """
		self.update()
		if hasattr(self.info, "error") and hasattr(self.info.error,
													"localizedMessage"):
			return self.info.error.localizedMessage

	@property
	def get_result(self):
		""" If result, return that result """
		self.update()
		if hasattr(self.info, "result"):
			return self.info.result

	@property
	def get_progress(self):
		""" Return the progress """
		self.update()
		if hasattr(self.info, "progress"):
			return self.info.progress

	def cancel(self):
		""" Atempt to cancel the task """
		try:
			self.update()
			self.CancelTask()
		except TaskFailedError, e:
			raise e
