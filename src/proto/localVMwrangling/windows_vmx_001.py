#!/usr/bin/env python
"""
vmx.py - Multi-hypervisor CLI wrapper for Windows
Supports: VMware Workstation/Player (vmrun), VirtualBox (VBoxManage), Hyper-V (PowerShell)

Usage examples:
  python vmx.py list
  python vmx.py start hyperv:WinDev
  python vmx.py suspend virtualbox:TestBox
  python vmx.py reset vmware:C:\\VMs\\MyVM\\MyVM.vmx --hard
  python vmx.py snapshot hyperv:SQLServer "Pre-patch 2026-02"
  python vmx.py snapshots hyperv:DevBox
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Tuple

# Paths — adjust if needed
VMRUN = r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"  # or Workstation Pro path
VBOXMANAGE = "VBoxManage"  # usually in PATH

# PowerShell prefix — ensures Hyper-V module is loaded
PS_PREFIX = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command"]

def run(cmd: list, check=True, capture_output=False, text=True, shell=False):
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=text,
            encoding="utf-8" if text else None,
            shell=shell
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        if e.stderr:
            print(e.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Command not found: {cmd[0]}", file=sys.stderr)
        sys.exit(1)


def run_powershell(script: str, capture_output=False):
    """Run inline PowerShell script"""
    cmd = PS_PREFIX + [script]
    return run(cmd, capture_output=capture_output, shell=False)


def detect_hypervisor_and_clean_vm(vm_str: str) -> Tuple[str, str]:
    vm = vm_str.strip()

    if vm.lower().startswith("vmware:"):
        return "vmware", vm[7:].strip()
    if vm.lower().startswith("virtualbox:"):
        return "virtualbox", vm[11:].strip()
    if vm.lower().startswith("hyperv:"):
        return "hyperv", vm[7:].strip()

    p = Path(vm)
    if p.suffix.lower() == ".vmx":
        return "vmware", vm
    if p.suffix.lower() in (".vbox", ".vdi"):
        return "virtualbox", vm

    # Default fallback → Hyper-V VM name
    return "hyperv", vm


def list_vms():
    print("=== VMware VMs ===")
    run([VMRUN, "list"], capture_output=False)

    print("\n=== VirtualBox VMs ===")
    run([VBOXMANAGE, "list", "vms"], capture_output=False)

    print("\n=== Hyper-V VMs ===")
    run_powershell("Get-VM | Select-Object Name, State, Status | Format-Table -AutoSize")


def start_vm(hyper: str, vm: str, headless: bool = True):
    if hyper == "vmware":
        gui_flag = "gui" if not headless else "nogui"
        run([VMRUN, "-T", "ws", "start", vm, gui_flag])
    elif hyper == "virtualbox":
        args = [VBOXMANAGE, "startvm", vm]
        if headless:
            args += ["--type", "headless"]
        run(args)
    elif hyper == "hyperv":
        # Hyper-V has no native headless CLI flag; starts in background, connect via VMConnect
        run_powershell(f"Start-VM -Name '{vm}'")
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def stop_vm(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "stop", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "acpipowerbutton"])
    elif hyper == "hyperv":
        run_powershell(f"Stop-VM -Name '{vm}' -Force")
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def suspend_vm(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "suspend", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "savestate"])
    elif hyper == "hyperv":
        run_powershell(f"Suspend-VM -Name '{vm}'")
    else:
        sys.exit(f"Suspend not supported for {hyper}")


def reset_vm(hyper: str, vm: str, hard: bool = False):
    if hyper == "vmware":
        power_type = "hard" if hard else "soft"
        run([VMRUN, "reset", vm, power_type])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "reset"])
    elif hyper == "hyperv":
        run_powershell(f"Restart-VM -Name '{vm}' -Force")
    else:
        sys.exit(f"Reset not supported for {hyper}")


def create_snapshot(hyper: str, vm: str, snapshot_name: str):
    if hyper == "vmware":
        run([VMRUN, "snapshot", vm, snapshot_name])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "snapshot", vm, "take", snapshot_name])
    elif hyper == "hyperv":
        run_powershell(f"Checkpoint-VM -Name '{vm}' -SnapshotName '{snapshot_name}'")
    else:
        sys.exit(f"Snapshots not supported for {hyper}")


def list_snapshots(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "listSnapshots", vm, "showtree"], capture_output=False)
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "snapshot", vm, "list", "--details"], capture_output=False)
    elif hyper == "hyperv":
        run_powershell(
            f"Get-VMCheckpoint -VMName '{vm}' | "
            "Select-Object VMName, Name, CreationTime, ParentCheckpointName | "
            "Format-Table -AutoSize"
        )
    else:
        sys.exit(f"Snapshots not supported for {hyper}")


def status_vm(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "list"], capture_output=False)
        print(f"\nFor '{vm}':")
        run([VMRUN, "getGuestIPAddress", vm, "-wait"], check=False)
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "showvminfo", vm], capture_output=False)
    elif hyper == "hyperv":
        run_powershell(
            f"Get-VM -Name '{vm}' | "
            "Select-Object Name, State, Status, Uptime | "
            "Format-List"
        )
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def get_ip(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "getGuestIPAddress", vm, "-wait"])
    elif hyper == "virtualbox":
        run([
            VBOXMANAGE, "guestproperty", "get", vm,
            "/VirtualBox/GuestInfo/Net/0/IP"
        ])
    elif hyper == "hyperv":
        # Requires Integration Services; gets first IPv4 address
        run_powershell(
            f"$vm = Get-VM -Name '{vm}'; "
            "$vm | Get-VMNetworkAdapter | "
            "ForEach-Object { "
            "  $_.IpAddresses | Where-Object { $_ -match '^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$' } "
            "} | Select-Object -First 1"
        )
    else:
        sys.exit(f"IP query not supported for {hyper}")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-hypervisor VM control on Windows (VMware / VirtualBox / Hyper-V)",
        epilog="VM identifiers: path/to/vm.vmx | vmware:name | virtualbox:name | hyperv:name | just name (defaults to Hyper-V)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser(
        "list",
        help="List all VMs across hypervisors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py list
"""
    )

    # start
    p_start = subparsers.add_parser(
        "start",
        help="Start a VM (headless where possible)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py start hyperv:Win11Dev
  python vmx.py start virtualbox:TestLinux --no-headless
  python vmx.py start vmware:C:\\VMs\\Ubuntu\\Ubuntu.vmx
"""
    )
    p_start.add_argument("vm", help="VM identifier")
    p_start.add_argument("--no-headless", action="store_true", help="Start with GUI (if supported)")

    # stop
    p_stop = subparsers.add_parser(
        "stop",
        help="Gracefully stop a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py stop hyperv:SQLServer
  python vmx.py stop virtualbox:Debian
"""
    )
    p_stop.add_argument("vm", help="VM identifier")

    # suspend
    p_suspend = subparsers.add_parser(
        "suspend",
        help="Suspend / save state of a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py suspend hyperv:DevBox
  python vmx.py suspend vmware:MyServer
"""
    )
    p_suspend.add_argument("vm", help="VM identifier")

    # reset
    p_reset = subparsers.add_parser(
        "reset",
        help="Reset / reboot a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py reset hyperv:TestVM --hard
  python vmx.py reset virtualbox:WinTest
"""
    )
    p_reset.add_argument("vm", help="VM identifier")
    p_reset.add_argument("--hard", action="store_true", help="Hard/force reset")

    # snapshot
    p_snapshot = subparsers.add_parser(
        "snapshot",
        help="Create a new snapshot/checkpoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py snapshot hyperv:Production "Before update Feb 2026"
  python vmx.py snapshot vmware:MyVM "Clean state"
"""
    )
    p_snapshot.add_argument("vm", help="VM identifier")
    p_snapshot.add_argument("name", help="Snapshot name")

    # snapshots
    p_snapshots = subparsers.add_parser(
        "snapshots",
        help="List snapshots/checkpoints for a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py snapshots hyperv:DevBox
  python vmx.py snapshots virtualbox:MyLinux
"""
    )
    p_snapshots.add_argument("vm", help="VM identifier")

    subparsers.add_parser(
        "list-snapshots",
        help="Alias for snapshots",
        parents=[p_snapshots],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=p_snapshots.epilog
    )

    # status
    p_status = subparsers.add_parser(
        "status",
        help="Show VM status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py status hyperv:WinServer
  python vmx.py status vmware:Test
"""
    )
    p_status.add_argument("vm", help="VM identifier")

    # ip
    p_ip = subparsers.add_parser(
        "ip",
        help="Get guest IP (requires guest tools/integration services)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python vmx.py ip hyperv:UbuntuGuest
  python vmx.py ip virtualbox:Win10
"""
    )
    p_ip.add_argument("vm", help="VM identifier")

    args = parser.parse_args()

    if args.command == "list":
        list_vms()
        return

    hyper, clean_vm = detect_hypervisor_and_clean_vm(args.vm)

    if not clean_vm:
        parser.error("No VM specified")

    cmd = args.command

    if cmd == "start":
        start_vm(hyper, clean_vm, headless=not args.no_headless)
        print(f"Started {hyper}:{clean_vm}")

    elif cmd == "stop":
        stop_vm(hyper, clean_vm)
        print(f"Stopped {hyper}:{clean_vm}")

    elif cmd == "suspend":
        suspend_vm(hyper, clean_vm)
        print(f"Suspended {hyper}:{clean_vm}")

    elif cmd == "reset":
        reset_vm(hyper, clean_vm, hard=args.hard)
        print(f"Reset {hyper}:{clean_vm} ({'hard' if args.hard else 'soft'})")

    elif cmd == "snapshot":
        create_snapshot(hyper, clean_vm, args.name)
        print(f"Created snapshot '{args.name}' for {hyper}:{clean_vm}")

    elif cmd in ("snapshots", "list-snapshots"):
        list_snapshots(hyper, clean_vm)

    elif cmd == "status":
        status_vm(hyper, clean_vm)

    elif cmd == "ip":
        get_ip(hyper, clean_vm)


if __name__ == "__main__":
    main()


