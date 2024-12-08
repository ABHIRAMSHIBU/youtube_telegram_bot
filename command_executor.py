from subprocess import Popen, PIPE

class Executor:
    def __init__(self):
        self.process = None
        self.executed = False
    def execute(self, command):
        if self.executed:
            raise Exception("Command already executed")
        self.executed = True
        self.command = command
        self.process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    def join(self):
        self.process.wait()
    def kill(self):
        self.process.kill()
    def get_output(self):
        self.output = self.process.stdout.read()
        return self.output
    def get_error(self):
        self.error = self.process.stderr.read()
        return self.error
    def get_pid(self):
        return self.process.pid
    def get_status(self):
        return self.process.returncode
    def get_command(self):
        return self.command
        
        