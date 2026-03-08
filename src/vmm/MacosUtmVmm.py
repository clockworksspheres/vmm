import inspect
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.run_commands import RunWith
from VirtualMachineManageTemplate import VirtualMachineManageTemplate


class MacosUtmVmm(VirtualMachineManageTemplate):

    def __init__(self, logger, **kwargs):
        """
        """
        if isinstance(logger, type(CyLogger)):
            self.logger = logger
        else:
            self.logger = CyLogger()
            self.logger.initializeLogs()

        # self.logger.log(lp.ERROR, f"Initializing {self.__class__.__name__} class")

        self.run = RunWith(self.logger)

        self.utmctl = "utmctl"

    def list_vms(self):
        """
        List available VMs 
        """
        cmd = [self.utmctl, "list"]
        self.run.setCommand(cmd)
        out, _, _ = self.run.communicate()
        print(f"{out}")

    def start_vm(self, vm: str = "", headless: bool = False):
        """
         Start a virtual machine

        """
        cmd = [self.utmctl, "start", vm]
        self.run.setCommand(cmd)
        self.run.communicate()

    def stop_vm(self, vm: str = "", hard: bool = True):
        """
         Stop a virtual machine
        """
        cmd = [self.utmctl, "stop", vm]
        self.run.setCommand(cmd)
        self.run.communicate()

    def pause_vm(self, vm: str = ""):
        """
        Suspend a virtual machine
        """
        cmd = [self.utmctl, "pause", vm]
        self.run.setCommand(cmd)
        self.run.communicate()

    def unpause_vm(self, vm: str = ""):
        """
        Suspend a virtual machine
        """
        cmd = [self.utmctl, "start", vm]
        self.run.setCommand(cmd)
        self.run.communicate()

    def reset_vm(self, vm: str = "", hard: bool = True):
        """
        Reset a virtual machine 
        """
        cmd1 = [self.utmctl, "stop", vm]
        self.run.setCommand(cmd1)
        self.run.communicate()
        cmd2 = [self.utmctl, "start", vm]
        self.run.setCommand(cmd2)
        self.run.communicate()

    def get_vm_status(self, vm: str):
        """
        Get the status of a virtual machine 
        """
        cmd = [self.utmctl, "status", vm]
        self.run.setCommand(cmd)
        out, err, retval = self.run.communicate()
        print(f"{out.strip()}")
        return out.strip()

    def get_ip(self, vm: str = ""):
        """
        get the IP address of a virtual machine 

        Not supported for macOS vm's, so it's not
        supported for all UTM vms
        """
        message = "Not supported for the UTM hypervisor"
        print(message)
        return message
        #cmd = [self.utmctl, "ip-address", vm]
        #self.run.setCommand(cmd)
        #out, err, retval = self.run.communicate()
        #print(f"{out.strip()}")
        #return out.strip()

