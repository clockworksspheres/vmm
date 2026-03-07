def safe_get(obj, key, default=None):
    """Safely get a key from a dict or list of dicts."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and key in item:
                return item[key]
    return default


def detect_os_from_config(config):
    """Detect OS from UTM config.plist."""

    # 1. Direct OS template (if UTM stored it)
    system = config.get("System", {})
    os_type = system.get("OperatingSystem")
    if os_type:
        return os_type

    # 2. Infer from attached images
    drives = config.get("Drives", [])
    for drive in drives:
        path = drive.get("Path", "").lower()

        if path.endswith(".ipsw") or "macos" in path:
            return "macOS"

        if "win" in path or "windows" in path:
            return "Windows"

        if any(distro in path for distro in [
            "ubuntu", "fedora", "arch", "debian", "linux"
        ]):
            return "Linux"

    # 3. Infer from QEMU hardware profile
    display = config.get("Display", {})
    network = config.get("Network", {})
    architecture = system.get("Architecture", "").lower()

    display_type = safe_get(display, "Type")
    network_device = safe_get(network, "Device")

    # macOS VMs use Apple Virtualization, not QEMU
    if system.get("Hypervisor") == "Apple":
        return "macOS"

    # Windows clues
    if system.get("TPMEnabled") is True:
        return "Windows"

    # Linux clues
    if display_type == "Spice" and network_device == "virtio-net":
        return "Linux"

    # If architecture is ARM and no macOS clues → likely Linux
    if architecture in ("aarch64", "arm64"):
        return "Linux"

    return "Unknown"

