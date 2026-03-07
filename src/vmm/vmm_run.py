import psutil
import sys

hypervisorMap = {"vmware": "VMware Fusion", "virtualbox": "VirtualBox", "utm": "UTM"}


def vmm_run(args):
    hyper = args.hypervisor
    vm = args.vm

    matched = None

    hypervisorApp = hypervisorMap[args.hypervisor.strip()]

    for proc in psutil.process_iter(['pid', 'name']):
        #if re.match(re.escape(hypervisor), proc.info['name']):
        if hypervisorApp == proc.info['name'].strip():
            print(f"{proc.info['name']}")
            matched = proc.info['name']

    if not matched:
        message = f"Hypervisor {hypervisorApp} not running, start {hypervisorApp} first"
        print(message)
        raise HypervisorNotValid(message)

    vmm = VirtualMachineManage(hyper)

    cmd = args.command

    if args.command == "list":
        vmm.list_vms(hyper)
        return

    if cmd == "start":
        vmm.start_vm(vm, headless=args.headless)
        print(f"Started {hyper} → {vm}")

    elif cmd == "stop":
        vmm.stop_vm(vm)
        print(f"Stopped {hyper} → {vm}")

    elif cmd == "pause":
        vmm.pause_vm(vm)
        print(f"Suspended {hyper} → {vm}")

    elif cmd == "unpause":
        vmm.unpause_vm(vm)
        print(f"Suspended {hyper} → {vm}")

    elif cmd == "reset":
        vmm.reset_vm(vm, hard=args.hard)
        print(f"Reset {hyper} → {vm}")

    elif cmd == "status":
        vmm.list_vms()

    elif cmd == "ip":
        vmm.get_ip(vm)


