import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import os

#####
# Include the parent project directory in the PYTHONPATH
appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(appendDir)
sys.path.append('./..')
sys.path.append('./../vmm')

# Import the module under test
import vmm.vmm as vmm


class TestVmmCLI(unittest.TestCase):

    def setUp(self):
        # Patch VirtualMachineManage for all tests
        patcher = patch("vmm.vmm.VirtualMachineManage")
        self.MockVMM = patcher.start()
        self.addCleanup(patcher.stop)

        # Instance returned when VirtualMachineManage(hypervisor) is called
        self.mock_instance = self.MockVMM.return_value

    def run_cli(self, argv):
        """Helper to run main() with mocked argv and capture output."""
        with patch.object(sys, "argv", argv):
            buf = io.StringIO()
            with patch("sys.stdout", buf):
                try:
                    vmm.main()
                except SystemExit:
                    pass
            return buf.getvalue()

    @unittest.SkipTest
    def test_list(self):
        output = self.run_cli(["vmm.py", "list", "vmware"])
        self.mock_instance.list_vms.assert_called_once_with("vmware")

    def test_start_headless(self):
        output = self.run_cli(["vmm.py", "start", "vmware", "MyVM", "--headless"])
        self.mock_instance.start_vm.assert_called_once_with("MyVM", headless=True)
        self.assertIn("Started vmware → MyVM", output)

    def test_start_no_headless(self):
        output = self.run_cli(["vmm.py", "start", "virtualbox", "TestVM"])
        self.mock_instance.start_vm.assert_called_once_with("TestVM", headless=False)

    def test_stop(self):
        output = self.run_cli(["vmm.py", "stop", "utm", "DevBox"])
        self.mock_instance.stop_vm.assert_called_once_with("DevBox")
        self.assertIn("Stopped utm → DevBox", output)

    def test_pause(self):
        output = self.run_cli(["vmm.py", "pause", "vmware", "MyVM"])
        self.mock_instance.pause_vm.assert_called_once_with("MyVM")

    def test_unpause(self):
        output = self.run_cli(["vmm.py", "unpause", "virtualbox", "MyVM"])
        self.mock_instance.unpause_vm.assert_called_once_with("MyVM")

    def test_reset_soft(self):
        output = self.run_cli(["vmm.py", "reset", "utm", "Box"])
        self.mock_instance.reset_vm.assert_called_once_with("Box", hard=False)

    def test_reset_hard(self):
        output = self.run_cli(["vmm.py", "reset", "utm", "Box", "--hard"])
        self.mock_instance.reset_vm.assert_called_once_with("Box", hard=True)

    def test_status(self):
        output = self.run_cli(["vmm.py", "status", "vmware", "MyVM"])
        self.mock_instance.list_vms.assert_called_once()

    def test_ip(self):
        output = self.run_cli(["vmm.py", "ip", "virtualbox", "Win11"])
        self.mock_instance.get_ip.assert_called_once_with("Win11")


if __name__ == "__main__":
    unittest.main()

