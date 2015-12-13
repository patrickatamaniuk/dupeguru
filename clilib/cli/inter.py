import logging
from hscommon.jobprogress.job import nulljob, JobCancelled

class DupeGuruView:
    JOB = nulljob

    def __init__(self):
        self.messages = []

    def start_job(self, jobid, func, args=()):
        try:
            func(self.JOB, *args)
        except JobCancelled:
            return

    def get_default(self, key_name):
        return None

    def set_default(self, key_name, value):
        pass

    def show_message(self, msg):
        self.messages.append(msg)

    def ask_yes_no(self, prompt):
        return True # always answer yes
