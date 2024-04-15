import subprocess

def get_linux_distribution():
    # Read contents of /etc/os-release file
    with open('/etc/os-release', 'r') as f:
        lines = f.readlines()
    
    # Parse contents to extract distribution info
    dist_info = {}
    for line in lines:
        key, value = line.strip().split('=', 1)
        dist_info[key.lower()] = value.strip('"')

    return dist_info.get('name', '').lower()

def install_slurm():
    # Detect Linux distribution
    dist = get_linux_distribution()

    # Choose appropriate package manager for the distribution
    if dist in ['debian', 'ubuntu']:
        package_manager = 'apt-get'
    elif dist in ['centos', 'redhat', 'fedora']:
        package_manager = 'yum'
    else:
        raise RuntimeError(f"Unsupported distribution: {dist}")

    # Update package repo and install Slurm with sudo permissions
    subprocess.run(['sudo', package_manager, 'update', '-y'], check=True)
    subprocess.run(['sudo', package_manager, 'install', 'slurmd', 'slurmctld', '-y'], check=True)

if __name__ == "__main__":
    install_slurm()
