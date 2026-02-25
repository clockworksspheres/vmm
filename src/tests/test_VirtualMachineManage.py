import unittest
from unittest.mock import patch, MagicMock
import sys
import os

#####
# Include the parent project directory in the PYTHONPATH
appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(appendDir)
sys.path.append('./..')
sys.path.append('./../vmm')

# Import the class under test
from vmm.VirtualMachineManage import VirtualMachineManage


class TestVirtualMachineManage(unittest.TestCase):

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_unimplemented_framework(self, mock_runwith, mock_logger):
        logger_instance = MagicMock()
        mock_logger.return_value = logger_instance

        with patch("sys.platform", "darwin"):
            vm = VirtualMachineManage("unknown")
            logger_instance.log.assert_called_once()

    #
    # Delegation tests
    #

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_list_vms(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.list_vms(test=1)
        vm.vmm.list_vms.assert_called_once_with(test=1)

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_start_vm(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.start_vm("testvm")
        vm.vmm.start_vm.assert_called_once_with("testvm")

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_stop_vm(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.stop_vm("testvm")
        vm.vmm.stop_vm.assert_called_once_with("testvm")

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_pause_vm(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.pause_vm("testvm")
        vm.vmm.pause_vm.assert_called_once_with("testvm")

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_unpause_vm(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.unpause_vm("testvm")
        vm.vmm.unpause_vm.assert_called_once_with("testvm")

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_reset_vm(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.reset_vm("testvm", hard=True)
        vm.vmm.reset_vm.assert_called_once_with("testvm", True)

    @patch("vmm.VirtualMachineManage.CyLogger")
    @patch("vmm.VirtualMachineManage.RunWith")
    def test_get_ip(self, mock_runwith, mock_logger):
        vm = VirtualMachineManage("vmware")
        vm.vmm = MagicMock()
        vm.get_ip("testvm")
        vm.vmm.get_ip.assert_called_once_with("testvm")


if __name__ == "__main__":
    unittest.main()

