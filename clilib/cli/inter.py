import logging
from hscommon.jobprogress.job import nulljob, JobCancelled

class DupeGuruView:
    JOB = nulljob

    def __init__(self, args=None):
        self.messages = []
        self.args = args

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
        print(msg)

    def ask_yes_no(self, prompt):
        return True # always answer yes

    def select_dest_file(self, msg, output_format):
        print(msg, output_format)
        return self.args.outfile or 'tmp.file'
