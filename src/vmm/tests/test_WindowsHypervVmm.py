import sys
import unittest

sys.path.append("./..")

# Skip whole suite if not running on Windows
@unittest.skipUnless(
    sys.platform.lower().startswith("win32"),
    "WindowsHypervVmm tests only run on Windows (win32)"
)
class TestWindowsHypervVmm(unittest.TestCase):

    from vmm.WindowsHypervVmm import WindowsHypervVmm

    class FakeRunWith:
        """Fake runner capturing commands instead of executing them."""
        def __init__(self, logger):
            self.logger = logger
            self.last_command = None
            self.responses = {}

        def setCommand(self, cmd):
            self.last_command = list(cmd)

        def communicate(self):
            key = tuple(self.last_command)
            return self.responses.get(key, ("", "", 0))

    class DummyLogger:
        def initializeLogs(self):
            pass
        def log(self, *args, **kwargs):
            pass

    def setUp(self):
        self.logger = self.DummyLogger()
        self.vmm = self.WindowsHypervVmm(self.logger)
        self.vmm.run = self.FakeRunWith(self.logger)

    def test_list_vms_sets_correct_command(self):
        """
        Typical Hyper-V list VMs call might be PowerShell Get-VM,
        e.g. ["powershell", "Get-VM"] — replace with real expectation.
        """
        self.vmm.list_vms()
        self.assertEqual(
            self.vmm.run.last_command,
            ["powershell", "Get-VM"]
        )

    def test_start_vm_sets_correct_command(self):
        self.vmm.start_vm("MyVM")
        self.assertEqual(
            self.vmm.run.last_command,
            ["powershell", "Start-VM", "-Name", "MyVM"]
        )

    def test_stop_vm_sets_correct_command(self):
        self.vmm.stop_vm("VM2", hard=True)
        # Expect Stop-VM PowerShell call with "-Force" for hard stop
        self.assertEqual(
            self.vmm.run.last_command,
            ["powershell", "Stop-VM", "-Name", "VM2", "-Force"]
        )

    def test_pause_vm_sets_correct_command(self):
        self.vmm.pause_vm("VMp")
        self.assertEqual(
            self.vmm.run.last_command,
            ["powershell", "Suspend-VM", "-Name", "VMp"]
        )

    def test_unpause_vm_sets_correct_command(self):
        self.vmm.unpause_vm("VMu")
        self.assertEqual(
            self.vmm.run.last_command,
            ["powershell", "Resume-VM", "-Name", "VMu"]
        )

    def test_get_vm_status_returns_stripped_output(self):
        key = ("powershell", "Get-VM", "-Name", "vmS", "|", "Select-Object", "-ExpandProperty", "State")
        self.vmm.run.responses[key] = (" Running \n", "", 0)
        status = self.vmm.get_vm_status("vmS")
        self.assertEqual(status, "Running")

    def test_get_ip_returns_stripped_output(self):
        key = ("powershell", "Get-VMNetworkAdapter", "-VMName", "vmIP", "|", "Select-Object", "-ExpandProperty", "IpAddresses")
        self.vmm.run.responses[key] = (" 192.168.1.99 \n", "", 0)
        ip = self.vmm.get_ip("vmIP")
        self.assertEqual(ip, "192.168.1.99")


if __name__ == "__main__":
    unittest.main()

