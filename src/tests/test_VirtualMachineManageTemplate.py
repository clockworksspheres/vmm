import unittest
from unittest.mock import patch
import sys
import os

#####
# Include the parent project directory in the PYTHONPATH
appendDir = "/".join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(appendDir)
sys.path.append('./..')
sys.path.append('./../vmm')

import vmm.VirtualMachineManageTemplate as tmpl
from vmm.VirtualMachineManageTemplate import MethodNotImplementedError


class TestVirtualMachineManageTemplate(unittest.TestCase):

    def setUp(self):
        # Patch the imported names INSIDE the module
        # These MUST match the import paths used in VirtualMachineManageTemplate.py
        self.patcher_logger = patch("vmm.VirtualMachineManageTemplate.CyLogger")
        self.MockLogger = self.patcher_logger.start()

        self.patcher_run = patch("vmm.VirtualMachineManageTemplate.RunWith")
        self.MockRun = self.patcher_run.start()

        self.addCleanup(self.patcher_logger.stop)
        self.addCleanup(self.patcher_run.stop)

        # Create instance under test
        self.obj = tmpl.VirtualMachineManageTemplate()
        self.logger = self.MockLogger.return_value

    # Helper to test each method
    def assert_method_raises_and_logs(self, method, *args, **kwargs):
        with self.assertRaises(MethodNotImplementedError):
            method(*args, **kwargs)

        # Ensure the "not yet in production" message was logged
        self.logger.log.assert_any_call(
            tmpl.lp.INFO,
            f"--{self.obj.__class__.__name__} not yet in production."
        )

    # ---- Tests for each template method ----

    def test_list_vms(self):
        self.assert_method_raises_and_logs(self.obj.list_vms)

    def test_start_vm(self):
        self.assert_method_raises_and_logs(self.obj.start_vm, "VM1", headless=True)

    def test_stop_vm(self):
        self.assert_method_raises_and_logs(self.obj.stop_vm, "VM1", hard=False)

    def test_pause_vm(self):
        self.assert_method_raises_and_logs(self.obj.pause_vm, "VM1")

    def test_unpause_vm(self):
        self.assert_method_raises_and_logs(self.obj.unpause_vm, "VM1")

    def test_reset_vm(self):
        self.assert_method_raises_and_logs(self.obj.reset_vm, "VM1", hard=True)

    def test_get_vm_status(self):
        self.assert_method_raises_and_logs(self.obj.get_vm_status, "VM1")

    def test_get_ip(self):
        self.assert_method_raises_and_logs(self.obj.get_ip, "VM1")

    # ---- Constructor behavior ----

    def test_constructor_initializes_logger_and_run(self):
        # CyLogger() should be instantiated once
        self.MockLogger.assert_called_once()

        # initializeLogs() should be called
        self.logger.initializeLogs.assert_called_once()

        # RunWith(logger) should be instantiated
        self.MockRun.assert_called_once_with(self.logger)


if __name__ == "__main__":
    unittest.main()

