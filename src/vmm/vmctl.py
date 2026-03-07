#!/usr/bin/env python3
import argparse
import sys

from PySide6.QtWidgets import QApplication

from VirtualMachineManage import VirtualMachineManage
from vmmux.main import VmCtlUi
from vmm_run import vmm_run


HYPERVISORS = {"vmware", "virtualbox", "utm"}


def main():
    # HYPERVISORS = {"vmware", "virtualbox", "utm"}

    parser = argparse.ArgumentParser(
        description="Control virtual machines across VMware Fusion, VirtualBox, and UTM"
    )
    parser.add_argument("-g", "--gui", dest="gui", action="store_true", 
                        default=False, 
                        help="Run the vmctl graphical user interface")

    subparsers = parser.add_subparsers(dest="command")

    # ── list ────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "list",
        help="List VMs from all hypervisors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware
  %(prog)s virtualbox
  %(prog)s utm
  %(prog)s                     # shows running VMware, all VirtualBox & UTM VMs
"""
    )   

    # Common arguments for most commands
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("hypervisor", choices=HYPERVISORS,
                        help="vmware | virtualbox | utm")
    common.add_argument("vm", help="VM name or full path to .vmx / .vbox file")

    # ── start ───────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "start",
        parents=[common],
        help="Start a virtual machine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/My.vmx" --headless
  %(prog)s virtualbox "Windows 11 Test" --no-headless
  %(prog)s utm "My Linux Guest"
"""
    )   
    p.add_argument("--headless", action="store_true", default=False,
                   help="Start with GUI window (where supported)")

    # ── stop ────────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "stop",
        parents=[common],
        help="Gracefully shut down a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/MyVm.vmx"
  %(prog)s virtualbox "WinTest"
  %(prog)s utm "DevBox"
"""
    )   

    # ── pause ─────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "pause",
        parents=[common],
        help="Suspend / save state of a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/MyVm.vmx"
  %(prog)s virtualbox "Test VM"
  %(prog)s utm "Experiment"
"""
    )

    # ── unpause ─────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "unpause",
        parents=[common],
        help="Suspend / save state of a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/MyVm.vmx"
  %(prog)s virtualbox "Test VM"
  %(prog)s utm "Experiment"
"""
    )

    # ── reset ───────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "reset",
        parents=[common],
        help="Reset / reboot a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/MyVm.vmx"
  %(prog)s virtualbox "Win11" --hard
  %(prog)s reset utm "DevContainer"
"""
    )
    p.add_argument("--hard", action="store_true", default=False,
                   help="Force hard reset (like power button)")

    # ── status ──────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "status",
        parents=[common],
        help="Show current VM status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/MyVm.vmx"
  %(prog)s virtualbox "Win10 Guest"
  %(prog)s utm "Linux Experiment"
"""
    )
    #p.add_argument("vm", help="VM identifier")

    # ── ip ──────────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "ip",
        parents=[common],
        help="Get guest IP address (requires guest tools)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "/full/path/to/MyVm.vmx"
  %(prog)s virtualbox "Windows Test"
  %(prog)s utm "DevBox"
"""
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.gui:
        app = QApplication(sys.argv)
        print("started app...")
        window = VmCtlUi()
        print("initiated window")
        window.show()
        print("showing window...")
        window.raise_()
        print("raising_ window")
        sys.exit(app.exec())
    else:
        vmm_run(args)
        sys.exit()


if __name__ == "__main__":
    main()

