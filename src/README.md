# Virtual Machine Manage (vmm)

## What is Virtual Machine Manage

An OO factory that pumps out concrete classes
to manage virtual machines based on the hypervisor
being used.

The hypervisor needs to be running prior to use
of this code.

Currently this is designed for macOS, and the 
following hypervisors:

 * VmWare Fusion
 * Virtualbox
 * UTM
 * HyperV

## Directories

```
├── BuildScripts # pyinstaller build scripts
├── docs     # Support documentation
├── proto    # Prototyping directory
├── vmm      # root of the source code
└── vmmBoard # eisenban kanban board directory
```

## Vmware VM Notes

the default path "/full/path/to/my.vmx" for managing 
VMware Fusion VM's, should look like:

"/Users/<username>/Virtual Machines.localized/MyVm.vmwarevm/MyVm.vmx"

Unless the user has saved the VM to a different location.


## VirtualBox VM Notes


## UTM VM Notes


## HyperV VM Notes


