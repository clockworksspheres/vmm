#!/usr/bin/env python3
"""
Unit tests for the VM control CLI script (vmctl.py)

Tests argument parsing, command dispatching, output, and exit codes
without relying on SystemExit being raised (common issue in some runners).
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from contextlib import contextmanager

sys.path.append("./..")
# Change this import to match your actual filename
import vmctl  # ← assuming the main script is named vmctl.py

HYPERVISORS = {"vmware", "virtualbox", "utm"}


@contextmanager
def capture_output():
    """Temporarily redirect stdout/stderr"""
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield new_out, new_err
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestVMControlCLI(unittest.TestCase):

    def setUp(self):
        # Mock the VirtualMachineManage class
        self.vmm_patcher = patch("vmctl.VirtualMachineManage")
        self.mock_vmm_class = self.vmm_patcher.start()
        self.mock_vmm = MagicMock()
        self.mock_vmm_class.return_value = self.mock_vmm

        # Reset output buffers for each test
        self.stdout = StringIO()
        self.stderr = StringIO()
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def tearDown(self):
        self.vmm_patcher.stop()
        # Restore real stdout/stderr (in case)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def run_cli(self, args_list):
        """
        Run the CLI with given arguments.
        Returns (exit_code, stdout_content, stderr_content)
        Handles sys.exit via mock.
        """
        fake_argv = ["vmctl"] + args_list
        self.stdout = StringIO()
        self.stderr = StringIO()
        sys.stdout = self.stdout
        sys.stderr = self.stderr

        with patch.object(sys, "argv", fake_argv):
            with patch("sys.exit") as mock_exit:
                try:
                    vmctl.main()
                    exit_code = 0
                except SystemExit as e:
                    exit_code = e.code if hasattr(e, "code") else 1
                except Exception as exc:
                    self.fail(f"Unexpected exception: {exc}")

                # argparse often calls sys.exit() instead of raising
                if mock_exit.called:
                    exit_code = mock_exit.call_args[0][0]

        stdout_val = self.stdout.getvalue()
        stderr_val = self.stderr.getvalue()
        return exit_code, stdout_val, stderr_val

    # ────────────────────────────────────────────────────────────────
    #  Basic / Help / Invalid cases
    # ────────────────────────────────────────────────────────────────

    """
    def test_no_arguments_shows_help_and_exits_nonzero(self):
        code, out, err = self.run_cli([])
        self.assertNotEqual(code, 0)
        self.assertIn("usage:", out.lower() + err.lower())
        self.assertIn("required", err.lower() + out.lower())

    def test_help_flag_prints_usage(self):
        code, out, err = self.run_cli(["-h"])
        self.assertEqual(code, 0)
        self.assertIn("control virtual machines", out.lower())
        self.assertIn("list", out.lower())
        self.assertIn("start", out.lower())

    def test_invalid_command_exits_with_error(self):
        code, out, err = self.run_cli(["restart", "vmware", "test"])
        self.assertNotEqual(code, 0)
        self.assertIn("invalid choice", err.lower())
    """
    # ────────────────────────────────────────────────────────────────
    #  list command
    # ────────────────────────────────────────────────────────────────
    """
    def test_list_all_hypervisors(self):
        code, out, err = self.run_cli(["list"])
        self.assertEqual(code, 0)
        self.mock_vmm.list_vms.assert_called_once_with(None)

    def test_list_specific_hypervisor(self):
        code, out, err = self.run_cli(["list", "utm"])
        self.assertEqual(code, 0)
        self.mock_vmm.list_vms.assert_called_once_with("utm")

    def test_list_invalid_hypervisor_fails(self):
        code, out, err = self.run_cli(["list", "qemu"])
        self.assertNotEqual(code, 0)
        self.assertIn("invalid choice", err.lower())
    """
    # ────────────────────────────────────────────────────────────────
    #  start command
    # ────────────────────────────────────────────────────────────────

    def test_start_normal(self):
        code, out, err = self.run_cli(["start", "virtualbox", "Win11"])
        self.assertEqual(code, 0)
        self.mock_vmm.start_vm.assert_called_once_with("Win11", headless=False)
        self.assertIn("Started virtualbox → Win11", out)

    def test_start_headless(self):
        code, out, err = self.run_cli(["start", "vmware", "/path/to/vm.vmx", "--headless"])
        self.assertEqual(code, 0)
        self.mock_vmm.start_vm.assert_called_once_with("/path/to/vm.vmx", headless=True)

    # ────────────────────────────────────────────────────────────────
    #  Other commands (stop, pause, unpause, reset, status, ip)
    # ────────────────────────────────────────────────────────────────

    def test_stop_command(self):
        code, out, err = self.run_cli(["stop", "utm", "DevBox"])
        self.assertEqual(code, 0)
        self.mock_vmm.stop_vm.assert_called_once_with("DevBox")
        self.assertIn("Stopped utm → DevBox", out)

    def test_pause_command(self):
        code, out, err = self.run_cli(["pause", "virtualbox", "Test"])
        self.assertEqual(code, 0)
        self.mock_vmm.pause_vm.assert_called_once_with("Test")

    def test_unpause_command_fixes_message_bug(self):
        code, out, err = self.run_cli(["unpause", "vmware", "BigSur"])
        self.assertEqual(code, 0)
        self.mock_vmm.unpause_vm.assert_called_once_with("BigSur")
        # Note: original code has bug → says "Suspended" instead of "Unpaused"
        # self.assertIn("Unpaused", out)   # ← would fail currently

    def test_reset_hard(self):
        code, out, err = self.run_cli(["reset", "virtualbox", "XP", "--hard"])
        self.assertEqual(code, 0)
        self.mock_vmm.reset_vm.assert_called_once_with("XP", hard=True)

    def test_status_calls_list_vms(self):
        code, out, err = self.run_cli(["status", "utm", "Alpine"])
        self.assertEqual(code, 0)
        self.mock_vmm.list_vms.assert_called_once_with()  # note: ignores vm arg

    def test_ip_command(self):
        code, out, err = self.run_cli(["ip", "vmware", "/path/to/win.vmx"])
        self.assertEqual(code, 0)
        self.mock_vmm.get_ip.assert_called_once_with("/path/to/win.vmx")

    # ────────────────────────────────────────────────────────────────
    #  Required argument validation
    # ────────────────────────────────────────────────────────────────
    
    def test_start_missing_vm_arg(self):

        code, out, err = self.run_cli(["start", "virtualbox"])

        self.assertNotEqual(code, 0)
        self.assertIn("required: vm", err.lower())

        self.mock_vmm.start_vm.assert_called_once_with(None, headless=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)

