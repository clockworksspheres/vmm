#!/usr/bin/env python3
"""
vmx.py - Multi-hypervisor VM control (hypervisor as subcommand argument)

Supported hypervisors: vmware, virtualbox, utm

Examples (global):
  vmx.py list
  vmx.py start vmware "My Ubuntu" --no-headless
  vmx.py snapshot utm "DevBox" "Before upgrade"
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Adjust these paths if necessary
VMRUN = "/Applications/VMware Fusion.app/Contents/Library/vmrun"              # or Fusion Pro path
VBOXMANAGE = "VBoxManage"
UTMCTL = "utmctl"  # e.g. /Applications/UTM.app/Contents/MacOS/utmctl

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
    p = Path(vm_arg)
    detected = None
    if p.suffix.lower() == ".vmx" or "vmwarevm" in p.name.lower():
        detected = "vmware"
    elif p.suffix.lower() in (".vbox", ".vdi"):
        detected = "virtualbox"

    if detected and detected != hyper:
        print(f"Warning: specified {hyper} but path looks like {detected}", file=sys.stderr)
    return vm_arg


def list_vms():
    print("=== VMware Fusion (running VMs only) ===")
    run([VMRUN, "list"], capture_output=False)

    print("\n=== VirtualBox (all registered VMs) ===")
    run([VBOXMANAGE, "list", "vms"], capture_output=False)

    print("\n=== UTM (all VMs) ===")
    try:
        run([UTMCTL, "list"], capture_output=False)
    except Exception:
        print("(utmctl not found — is UTM installed?)")


def start_vm(hyper: str, vm: str, headless: bool = False):
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
        sys.exit(f"Unknown hypervisor: {hyper}")


def stop_vm(hyper: str, vm: str, how: str = "hard"):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "stop", vm, how])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "acpipowerbutton"])
    elif hyper == "utm":
        run([UTMCTL, "stop", vm])
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def suspend_vm(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "suspend", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "savestate"])
    elif hyper == "utm":
        run([UTMCTL, "pause", vm])  # resume with start
    else:
        sys.exit(f"Suspend not supported for {hyper}")


def reset_vm(hyper: str, vm: str, hard: bool = True):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        ptype = "hard" if hard else "soft"
        run([VMRUN, "-T", "fusion", "reset", vm, ptype])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "reset"])
    elif hyper == "utm":
        run([UTMCTL, "stop", vm])
        run([UTMCTL, "start", vm])
    else:
        sys.exit(f"Reset not supported for {hyper}")

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
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def get_ip(hyper: str, vm: str):
    vm = normalize_vm(hyper, vm)
    if hyper == "vmware":
        run([VMRUN, "-T", "fusion", "getGuestIPAddress", vm, "-wait"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "guestproperty", "get", vm, "/VirtualBox/GuestInfo/Net/0/IP"])
    elif hyper == "utm":
        run([UTMCTL, "ip-address", vm])
    else:
        sys.exit(f"IP query not supported for {hyper}")


def main():
    parser = argparse.ArgumentParser(
        description="Control virtual machines across VMware Fusion, VirtualBox, and UTM",
        epilog="Use '%(prog) list' to see all VMs\nUse 'vmx.py <command> --help' for command-specific examples"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

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
  %(prog)s vmware "Ubuntu Server"               # headless
  %(prog)s vmware "/Users/roy/VMs/MyVM/My.vmx" --headless
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
  %(prog)s vmware "Production Server"
  %(prog)s virtualbox "WinTest"
  %(prog)s utm "DevBox"
"""
    )

    # ── suspend ─────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "suspend",
        parents=[common],
        help="Suspend / save state of a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "My Linux"
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
  %(prog)s vmware "Server01"
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
  %(prog)s vmware "My Server"
  %(prog)s virtualbox "Win10 Guest"
  %(prog)s utm "Linux Experiment"
"""
    )
    p.add_argument("vm", help="VM identifier")

    # ── ip ──────────────────────────────────────────────────────────────────
    p = subparsers.add_parser(
        "ip",
        parents=[common],
        help="Get guest IP address (requires guest tools)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s vmware "Ubuntu Server"
  %(prog)s virtualbox "Windows Test"
  %(prog)s utm "DevBox"
"""
    )

    args = parser.parse_args()

    if args.command == "list":
        list_vms()
        return

    hyper = args.hypervisor
    vm = args.vm

    cmd = args.command

    if cmd == "start":
        start_vm(hyper, vm, headless=args.headless)
        print(f"Started {hyper} → {vm}")

    elif cmd == "stop":
        stop_vm(hyper, vm)
        print(f"Stopped {hyper} → {vm}")

    elif cmd == "suspend":
        suspend_vm(hyper, vm)
        print(f"Suspended {hyper} → {vm}")

    elif cmd == "reset":
        reset_vm(hyper, vm, hard=args.hard)
        print(f"Reset {hyper} → {vm}")

    elif cmd == "status":
        status_vm(hyper, vm)

    elif cmd == "ip":
        get_ip(hyper, vm)


if __name__ == "__main__":
    main()


