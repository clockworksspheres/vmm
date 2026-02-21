"""
Factory Class to spawn concrete Virtual Machine Managers
(vmm), based on the passed in "framework"
"""
import inspect
from lib.loggers import CyLogger
from lib.loggers import LogPriority as lp
from lib.run_commands import RunWith
from VirtualMachineManageTemplate import VirtualMachineManageTemplate

class VirtualMachineManage(VirtualMachineManageTemplate):

    def __init__(self, framework, **kwargs):
        """
        """
        self.logger = CyLogger()
        self.logger.initializeLogs()

        #self.logger.log(lp.ERROR, f"Initializing {self.__class__.__name__} class")

        self.run = RunWith(self.logger)

        self.framework = framework

        if self.framework == "vmware":
            from MacosVmwareVmm import MacosVmwareVmm
            self.vmm = MacosVmwareVmm(self.logger)
        elif self.framework == "VirtualBox":
            from MacosVirtualboxVmm import MacosVirtualboxVmm
            self.vmm = MacosVirtualboxVmm(self.logger)
        elif self.framework == "utm":
            from MacosUtmVmm import MacosUtmVmm
            self.vmm = MacosUtmVmm(self.logger)
        else:
            self.logger.log(lp.ERROR, f"{self.framework} hasn't been implemented")

    def list_vms(self, vm, **kwargs):
        """
        List available VMs      
        """
        self.vmm.list_vms(vm, **kwargs)

    def start_vm(self, vm: str = "", headless: bool = False, **kwargs):
        """
         Start a virtual machine

        """
        self.vmm.start_vm(vm, **kwargs)

    def stop_vm(self, vm: str = "", hard: bool = True, **kwargs):
        """
         Stop a virtual machine
        """
        self.vmm.stop_vm(vm, **kwargs)

    def suspend_vm(self, vm: str = "", **kwargs):
        """
        Suspend a VM
        """
        self.vmm.suspend_vm(vm, **kwargs)

    def reset_vm(self, vm: str = "", hard: bool = True, **kwargs):
        """
        Reset a VM
        """
        self.vmm.reset_vm(vm, hard, **kwargs)

    def get_vm_status(self, vm: str):
        """
        Get the status of a VM
        """

    def get_ip(self, vm: str = "", **kwargs):
        """
        Get the IP of a VM 
        """
        self.vmm.get_ip(vm, **kwargs)


