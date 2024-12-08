# Create a vritual env .venv if ".venv" does not exist
import os
import venv
import subprocess
import sys
import getpass

class Installer:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.script_dir = script_dir
        self.service_file = "tele_youtube_bot.service"

    def create_virtual_env(self):
        os.chdir(self.script_dir)

        if not os.path.exists(".venv"):
            venv.create(".venv")

        self.python_root_bin = os.path.join(self.script_dir,".venv", "bin")

    def install_requirements(self):
        venv_python = os.path.join(".venv", "bin", "python")

        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])

    def create_service_file(self):
        user = getpass.getuser()

        data = open(self.service_file+".in").read()
        data = data.replace("%%USER%%",user)
        data = data.replace("%%BOT_ROOT%%", self.script_dir)
        data = data.replace("%%PYTHON_ROOT_BIN%%",self.python_root_bin)

        f = open(self.service_file,"w")
        f.write(data)
        f.close()

        print("Service Created!")

    def install_service(self):
        subprocess.check_call(["sudo","install", self.service_file, "/etc/systemd/system/"])
        print("Service Installed!")

    def print_help(self):
        print(f"To enable service use `systemctl enable {self.service_file}`")
        print(f"To start service use `systemctl start {self.service_file}`")
        print(f"To stop service use `systemctl stop {self.service_file}`")
        print(f"To disable service use `systemctl disable {self.service_file}`")
        print(f"To restart service use `systemctl restart {self.service_file}`")


    def main(self):
        self.create_virtual_env()
        self.install_requirements()
        self.create_service_file()
        self.install_service()
        self.print_help()

if __name__ == "__main__":
    ins = Installer()
    ins.main()