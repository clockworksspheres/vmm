import subprocess
import plistlib
import re
from pathlib import Path

def get_vm_ip(vm_name):
    # 1. Get VM info from utmctl
    result = subprocess.run(
        ["utmctl", "list", "--format", "plist"],
        capture_output=True,
        text=False
    )
    plist = plistlib.loads(result.stdout)

    # Find VM entry
    vm = next((v for v in plist if v["name"] == vm_name), None)
    if not vm:
        raise ValueError(f"VM '{vm_name}' not found")

    vm_path = Path(vm["path"])

    # 2. Read MAC address from the VM's configuration
    config_path = vm_path / "config.plist"
    config = plistlib.loads(config_path.read_bytes())

    try:
        mac = config["NetworkDevices"][0]["MACAddress"].lower()
    except Exception:
        raise RuntimeError("Could not read MAC address from VM config")

    # Normalize MAC (UTM stores uppercase, ARP uses lowercase)
    mac = mac.replace(":", "").lower()

    # 3. Scan ARP table
    arp_output = subprocess.check_output(["arp", "-a"], text=True)

    for line in arp_output.splitlines():
        # Example ARP line:
        # ? (192.168.64.3) at aa:bb:cc:dd:ee:ff on en0 ifscope [ethernet]
        m = re.search(r"\((.*?)\).*? at ([0-9a-f:]+)", line)
        if m:
            ip, mac_found = m.groups()
            if mac_found.replace(":", "").lower() == mac:
                return ip

    # 4. Fallback: scan DHCP leases
    leases_file = Path("/var/db/dhcpd_leases")
    if leases_file.exists():
        leases = leases_file.read_text()
        m = re.search(r"ip_address=(.*?)\n.*?hw_address=1," + mac, leases, re.S)
        if m:
            return m.group(1)

    return None

