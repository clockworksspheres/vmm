#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def run_vmrun(args):
    """Run a vmrun command and return stdout as text."""
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode().strip()


def get_vm_status(vmx_path):
    """Determine whether a VMware Fusion VM is running."""
    vmx_path = str(Path(vmx_path).expanduser())

    # List running VMs
    output = run_vmrun(["vmrun", "list"])

    running_vms = []
    for line in output.splitlines():
        if line.endswith(".vmx"):
            running_vms.append(line.strip())

    if vmx_path in running_vms:
        return "running"

    # If not running, check if suspended
    suspend_output = run_vmrun(["vmrun", "listSnapshots", vmx_path])
    if "Error" not in suspend_output and "No snapshots" not in suspend_output:
        # Suspended VMs still appear as stopped, but we can detect the state file
        vmx_dir = Path(vmx_path).parent
        if any(f.suffix == ".vmss" for f in vmx_dir.iterdir()):
            return "suspended"

    return "stopped"


def main():
    parser = argparse.ArgumentParser(
        description="Get the status of a VMware Fusion VM using vmrun."
    )
    parser.add_argument(
        "vmx",
        help="Path to the .vmx file of the VM"
    )
    args = parser.parse_args()

    vmx_path = Path(args.vmx)
    if not vmx_path.exists():
        print(f"Error: VMX file not found: {vmx_path}")
        return

    status = get_vm_status(vmx_path)
    print(f"VM Status: {status}")


if __name__ == "__main__":
    main()

