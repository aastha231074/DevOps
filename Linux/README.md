# Introduction to Linux

## What is Linux?

Linux is a kernel upon which you can build operating systems. The kernel is the core component that manages system resources and communication between hardware and software. Popular Linux-based operating systems (called distributions) include Ubuntu, Fedora, Debian, and Arch Linux.

## Linux File System Hierarchy

Linux uses a hierarchical file system structure where everything starts at the root directory (`/`). Unlike Windows with multiple drive letters (C:, D:, etc.), Linux organizes everything under a single root.

### Key Directories

- **`/boot`** – Contains the kernel, bootloader files, and system map needed to start the system
- **`/bin`** – Essential user command binaries (programs) needed for system boot and repair
- **`/dev`** – Device files representing hardware components (disks, terminals, printers, etc.)
- **`/etc`** – System-wide configuration files and shell scripts ("Editable Text Configuration")
- **`/home`** – Personal directories for all regular users (e.g., `/home/username`)
- **`/lib`** – Essential shared libraries needed by programs in `/bin` and `/sbin`
- **`/mnt`** – Temporary mount point for mounting file systems manually
- **`/proc`** – Virtual filesystem providing process and kernel information
- **`/sbin`** – System binaries for system administration (typically require root privileges)
- **`/usr`** – User programs, libraries, documentation, and shared resources
- **`/var`** – Variable data files like logs, databases, email, and temporary files

### Additional Important Directories

- **`/root`** – Home directory for the root (administrator) user
- **`/tmp`** – Temporary files that are often cleared on reboot
- **`/opt`** – Optional third-party software packages
- **`/media`** – Mount points for removable media (USB drives, CDs, etc.)

## Key Concepts

- **Case Sensitivity**: Linux is case-sensitive. `File.txt` and `file.txt` are different files.
- **No Drive Letters**: All storage is mounted within the single root hierarchy.
- **Everything is a File**: Devices, directories, and even processes are represented as files.