#!/usr/bin/env python3
"""
vmx.py - Multi-hypervisor VM control (hypervisor as subcommand argument)

Examples:
  vmx.py list
  vmx.py start vmware "My Ubuntu Server"          # headless
  vmx.py start virtualbox "Win11" --no-headless
  vmx.py stop utm "DevBox"
  vmx.py snapshot vmware "/path/to/MyVM/My.vmx" "2026 Baseline"
  vmx.py status virtualbox "Production VM"
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Adjust paths if needed
VMRUN = "/Applications/VMware Fusion.app/Contents/Library/vmrun"  # or Fusion Pro path
VBOXMANAGE = "VBoxManage"
UTMCTL = "utmctl"

HYPERVISORS = {"vmware", "virtualbox", "utm"}


def run(cmd, check=True, capture_output=False, text=True, shell=False):
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


def normalize_vm(hyper: str, vm_arg: str) -> str:
    """Allow path or name; warn if hyper doesn't match detected type"""
    p = Path(vm_arg)
    detected = None

    if p.suffix.lower() == ".vmx" or "vmwarevm" in p.name.lower():
        detected = "vmware"
    elif p.suffix.lower() in (".vbox", ".vdi"):
        detected = "virtualbox"

    if detected and detected != hyper:
        print(f"Warning: You specified -- {hyper} but path suggests {detected}", file=sys.stderr)

    return vm_arg  # we pass it as-is to the tool


def list_vms():
    print("=== VMware VMs (running only) ===")
    run([VMRUN, "list"], capture_output=False)

    print("\n=== VirtualBox VMs (all) ===")
    run([VBOXMANAGE, "list", "vms"], capture_output=False)

    print("\n=== UTM VMs ===")
    try:
        run([UTMCTL, "list"], capture_output=False)
    except SystemExit:
        print("(utmctl not found — is UTM installed?)")


def start_vm(hyper: str, vm: str, headless: bool = True):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        args = [VMRUN, "-T", "fusion", "start", vm, "nogui" if headless else "gui"]
        run(args)
    elif hyper == "virtualbox":
        args = [VBOXMANAGE, "startvm", vm]
        if headless:
            args += ["--type", "headless"]
        run(args)
    elif hyper == "utm":
        run([UTMCTL, "start", vm])
    else:
        sys.exit(f"Unsupported hypervisor: {hyper}")


def stop_vm(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "stop", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "acpipowerbutton"])
    elif hyper == "utm":
        run([UTMCTL, "stop", vm])


def suspend_vm(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "suspend", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "savestate"])
    elif hyper == "utm":
        run([UTMCTL, "pause", vm])  # UTM uses pause → resume with start


def reset_vm(hyper: str, vm: str, hard: bool = False):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        ptype = "hard" if hard else "soft"
        run([VMRUN, "-T", "fusion", "reset", vm, ptype])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "reset"])
    elif hyper == "utm":
        run([UTMCTL, "stop", vm])
        run([UTMCTL, "start", vm])


def create_snapshot(hyper: str, vm: str, snap_name: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "snapshot", vm, snap_name])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "snapshot", vm, "take", snap_name])
    elif hyper == "utm":
        print("UTM does not support snapshots via utmctl (use GUI or qcow2 tools)")
        sys.exit(1)


def list_snapshots(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "listSnapshots", vm, "showtree"], capture_output=False)
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "snapshot", vm, "list", "--details"], capture_output=False)
    elif hyper == "utm":
        print("UTM: no snapshot listing via utmctl")


def status_vm(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "list"], capture_output=False)
        print(f"\nGuest IP attempt for {vm}:")
        run([VMRUN, "-T", "fusion", "getGuestIPAddress", vm, "-wait"], check=False)
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "showvminfo", vm], capture_output=False)
    elif hyper == "utm":
        run([UTMCTL, "status", vm])


def get_ip(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "getGuestIPAddress", vm, "-wait"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "guestproperty", "get", vm, "/VirtualBox/GuestInfo/Net/0/IP"])
    elif hyper == "utm":
        run([UTMCTL, "ip-address", vm])


def main():
    parser = argparse.ArgumentParser(
        description="Multi-hypervisor VM control",
        epilog="Use 'list' without hypervisor; all other commands require one."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list (global - no hypervisor needed)
    subparsers.add_parser("list", help="List VMs from all hypervisors")

    # Common parser for commands that need hypervisor + vm
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("hypervisor", choices=HYPERVISORS, help="vmware | virtualbox | utm")
    common.add_argument("vm", help="VM name or full .vmx / .vbox path")

    # start
    p = subparsers.add_parser("start", parents=[common], help="Start VM")
    p.add_argument("--no-headless", action="store_true", help="Start with GUI")

    # stop, suspend, status, ip
    for cmd in ["stop", "suspend", "status", "ip"]:
        subparsers.add_parser(cmd, parents=[common], help=f"{cmd.capitalize()} VM")

    # reset
    p = subparsers.add_parser("reset", parents=[common], help="Reset VM")
    p.add_argument("--hard", action="store_true", help="Force hard reset")

    # snapshot
    p = subparsers.add_parser("snapshot", parents=[common], help="Create snapshot")
    p.add_argument("snap_name", metavar="name", help="Snapshot name")

    # snapshots
    subparsers.add_parser("snapshots", parents=[common], help="List snapshots")

    args = parser.parse_args()

    if args.command == "list":
        list_vms()
        return

    # All other commands require hypervisor + vm
    hyper = args.hypervisor
    vm = args.vm

    cmd = args.command

    if cmd == "start":
        start_vm(hyper, vm, headless=not args.no_headless)
        print(f"Started {hyper} VM: {vm}")

    elif cmd == "stop":
        stop_vm(hyper, vm)
        print(f"Stopped {hyper} VM: {vm}")

    elif cmd == "suspend":
        suspend_vm(hyper, vm)
        print(f"Suspended {hyper} VM: {vm}")

    elif cmd == "reset":
        reset_vm(hyper, vm, hard=args.hard)
        print(f"Reset {hyper} VM: {vm} ({'hard' if args.hard else 'soft'})")

    elif cmd == "snapshot":
        create_snapshot(hyper, vm, args.snap_name)
        print(f"Created snapshot '{args.snap_name}' for {hyper} VM: {vm}")

    elif cmd == "snapshots":
        list_snapshots(hyper, vm)

    elif cmd == "status":
        status_vm(hyper, vm)

    elif cmd == "ip":
        get_ip(hyper, vm)


if __name__ == "__main__":
    main()


