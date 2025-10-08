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

## Essential Linux Commands

### File and Directory Operations

| Command | Description | Example |
|---------|-------------|---------|
| `ls` | List directory contents | `ls -la` (detailed list with hidden files) |
| `cd` | Change directory | `cd /home/user` |
| `pwd` | Print working directory | `pwd` |
| `mkdir` | Create new directory | `mkdir newfolder` |
| `rmdir` | Remove empty directory | `rmdir oldfolder` |
| `rm` | Remove files or directories | `rm file.txt` or `rm -r folder/` |
| `cp` | Copy files or directories | `cp source.txt dest.txt` |
| `mv` | Move or rename files | `mv old.txt new.txt` |
| `touch` | Create empty file or update timestamp | `touch newfile.txt` |
| `cat` | Display file contents | `cat file.txt` |
| `less` | View file contents (paginated) | `less largefile.txt` |
| `head` | Display first lines of file | `head -n 10 file.txt` |
| `tail` | Display last lines of file | `tail -f /var/log/syslog` |

### File Permissions and Ownership

| Command | Description | Example |
|---------|-------------|---------|
| `chmod` | Change file permissions | `chmod 755 script.sh` |
| `chown` | Change file owner | `chown user:group file.txt` |
| `chgrp` | Change group ownership | `chgrp groupname file.txt` |

### System Information

| Command | Description | Example |
|---------|-------------|---------|
| `uname` | Display system information | `uname -a` |
| `df` | Show disk space usage | `df -h` |
| `du` | Show directory space usage | `du -sh /home` |
| `free` | Display memory usage | `free -h` |
| `top` | Display running processes | `top` |
| `ps` | Show process status | `ps aux` |
| `kill` | Terminate a process | `kill 1234` or `kill -9 1234` |

### File Search and Text Processing

| Command | Description | Example |
|---------|-------------|---------|
| `find` | Search for files | `find /home -name "*.txt"` |
| `grep` | Search text patterns | `grep "error" logfile.txt` |
| `locate` | Quick file search (uses database) | `locate filename` |
| `which` | Show full path of commands | `which python` |
| `wc` | Count lines, words, characters | `wc -l file.txt` |

### Network Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ping` | Test network connectivity | `ping google.com` |
| `ifconfig` / `ip` | Display/configure network interfaces | `ip addr show` |
| `netstat` | Network statistics | `netstat -tuln` |
| `ssh` | Secure shell connection | `ssh user@hostname` |
| `scp` | Secure copy files | `scp file.txt user@host:/path` |
| `wget` | Download files from web | `wget https://example.com/file.zip` |
| `curl` | Transfer data from/to servers | `curl https://api.example.com` |

### Package Management (Ubuntu/Debian)

| Command | Description | Example |
|---------|-------------|---------|
| `apt update` | Update package list | `sudo apt update` |
| `apt upgrade` | Upgrade installed packages | `sudo apt upgrade` |
| `apt install` | Install new package | `sudo apt install nginx` |
| `apt remove` | Remove package | `sudo apt remove package-name` |
| `apt search` | Search for packages | `apt search keyword` |

### User and Group Management

| Command | Description | Example |
|---------|-------------|---------|
| `whoami` | Display current username | `whoami` |
| `sudo` | Execute command as superuser | `sudo apt update` |
| `su` | Switch user | `su - username` |
| `useradd` | Add new user | `sudo useradd newuser` |
| `passwd` | Change user password | `passwd` |
| `groups` | Display user groups | `groups username` |

### Compression and Archives

| Command | Description | Example |
|---------|-------------|---------|
| `tar` | Create/extract archives | `tar -xzf archive.tar.gz` |
| `gzip` | Compress files | `gzip file.txt` |
| `gunzip` | Decompress files | `gunzip file.txt.gz` |
| `zip` | Create ZIP archives | `zip archive.zip file1 file2` |
| `unzip` | Extract ZIP archives | `unzip archive.zip` |