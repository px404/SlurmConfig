import os
import shutil
import subprocess
from install_slurm import install_slurm

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")

def find_slurm_directory():
    # Search for directories containing "slurm" in their name within /etc
    etc_path = '/etc'
    slurm_directories = [dir_name for dir_name in os.listdir(etc_path) if 'slurm' in dir_name]

    if slurm_directories:
        # Return the first directory found
        return os.path.join(etc_path, slurm_directories[0])
    else:
        # If no matching directory is found, return None
        return None

def generate_slurm_conf():
    # Get user inputs for Slurm configuration
    cluster_name = input("Enter ClusterName (Name of the Slurm cluster): ") or 'localcluster'
    slurmctld_host = input("Enter SlurmctldHost (Hostname or IP address of the Slurm controller): ") or 'localhost'
    mpi_default = input("Enter MpiDefault (Default MPI implementation to use, e.g., 'none', 'mvapich2', 'mpich', etc.): ") or 'none'
    proctrack_type = input("Enter ProctrackType (Type of process tracking used by Slurm, e.g., 'proctrack/linuxproc'): ") or 'proctrack/linuxproc'
    return_to_service = input("Enter ReturnToService (Time in seconds to wait before returning nodes to service): ") or '2'
    slurmctld_pid_file = input("Enter SlurmctldPidFile (Path to the PID file for the Slurm controller): ") or '/var/run/slurmctld.pid'
    slurmctld_port = input("Enter SlurmctldPort (Port number for the Slurm controller): ") or '6817'
    slurmd_pid_file = input("Enter SlurmdPidFile (Path to the PID file for Slurm daemon): ") or '/var/run/slurmd.pid'
    slurmd_port = input("Enter SlurmdPort (Port number for Slurm daemon): ") or '6818'
    slurmd_spool_dir = input("Enter SlurmdSpoolDir (Directory where Slurm daemon will store job-related files): ") or '/var/lib/slurm-llnl/slurmd'
    slurm_user = input("Enter SlurmUser (User account under which Slurm daemons run): ") or 'slurm'
    state_save_location = input("Enter StateSaveLocation (Directory where Slurm will store state information): ") or '/var/lib/slurm-llnl/slurmctld'
    switch_type = input("Enter SwitchType (Type of switch for node communication, e.g., 'switch/none'): ") or 'switch/none'
    task_plugin = input("Enter TaskPlugin (Type of task plugin used by Slurm, e.g., 'task/none'): ") or 'task/none'
    inactive_limit = input("Enter InactiveLimit (Time in seconds before an inactive job is considered eligible for termination): ") or '0'
    kill_wait = input("Enter KillWait (Time in seconds for Slurm to wait before killing a job after termination signal): ") or '30'
    min_job_age = input("Enter MinJobAge (Minimum age in seconds for a job to be considered for scheduling): ") or '300'
    slurmctld_timeout = input("Enter SlurmctldTimeout (Timeout in seconds for communication with Slurm controller): ") or '120'
    slurmd_timeout = input("Enter SlurmdTimeout (Timeout in seconds for communication with Slurm daemon): ") or '300'
    wait_time = input("Enter Waittime (Time in seconds to wait for job initiation): ") or '0'
    scheduler_type = input("Enter SchedulerType (Type of scheduler used by Slurm, e.g., 'sched/backfill'): ") or 'sched/backfill'
    select_type = input("Enter SelectType (Type of selection used by Slurm, e.g., 'select/cons_tres'): ") or 'select/cons_tres'
    select_type_parameters = input("Enter SelectTypeParameters (Parameters for SelectType, e.g., 'CR_Core'): ") or 'CR_Core'
    accounting_storage_type = input("Enter AccountingStorageType (Type of accounting storage used by Slurm, e.g., 'accounting_storage/none'): ") or 'accounting_storage/none'
    job_comp_type = input("Enter JobCompType (Type of job completion used by Slurm, e.g., 'jobcomp/none'): ") or 'jobcomp/none'
    job_acct_gather_frequency = input("Enter JobAcctGatherFrequency (Frequency in seconds for gathering job accounting data): ") or '30'
    job_acct_gather_type = input("Enter JobAcctGatherType (Type of job accounting data gathering, e.g., 'jobacct_gather/none'): ") or 'jobacct_gather/none'
    slurmctld_debug = input("Enter SlurmctldDebug (Level of debugging information for Slurm controller): ") or 'info'
    slurmctld_log_file = input("Enter SlurmctldLogFile (Path to the log file for Slurm controller): ") or '/var/log/slurm-llnl/slurmctld.log'
    slurmd_debug = input("Enter SlurmdDebug (Level of debugging information for Slurm daemon): ") or 'info'
    slurmd_log_file = input("Enter SlurmdLogFile (Path to the log file for Slurm daemon): ") or '/var/log/slurm-llnl/slurmd.log'
    node_name = input("Enter NodeName (Name of the compute node): ") or 'localhost'
    cpus = input("Enter CPUs (Number of CPU cores on the compute node): ") or '1'
    real_memory = input("Enter RealMemory (Amount of memory in megabytes on the compute node): ") or '500'
    state = input("Enter State (State of the compute node, e.g., 'UNKNOWN'): ") or 'UNKNOWN'
    partition_name = input("Enter PartitionName (Name of the partition to which the compute node belongs): ") or 'LocalQ'
    nodes = input("Enter Nodes (List of compute nodes, e.g., 'ALL'): ") or 'ALL'
    default = input("Enter Default (Whether the partition is the default partition, e.g., 'YES' or 'NO'): ") or 'YES'
    max_time = input("Enter MaxTime (Maximum time limit for jobs in the partition, e.g., 'INFINITE'): ") or 'INFINITE'
    
    # Create directories if they don't exist
    create_directory_if_not_exists(os.path.dirname(slurmctld_pid_file))
    create_directory_if_not_exists(os.path.dirname(slurmd_pid_file))
    create_directory_if_not_exists(slurmd_spool_dir)
    create_directory_if_not_exists(state_save_location)
    create_directory_if_not_exists(os.path.dirname(slurmctld_log_file))
    create_directory_if_not_exists(os.path.dirname(slurmd_log_file))
    
    # Write configuration to slurm.conf file
    with open('slurm.conf', 'w') as f:
        f.write(f'''\
# slurm.conf file generated by Python script.
ClusterName={cluster_name}
SlurmctldHost={slurmctld_host}
MpiDefault={mpi_default}
ProctrackType={proctrack_type}
ReturnToService={return_to_service}
SlurmctldPidFile={slurmctld_pid_file}
SlurmctldPort={slurmctld_port}
SlurmdPidFile={slurmd_pid_file}
SlurmdPort={slurmd_port}
SlurmdSpoolDir={slurmd_spool_dir}
SlurmUser={slurm_user}
StateSaveLocation={state_save_location}
SwitchType={switch_type}
TaskPlugin={task_plugin}
InactiveLimit={inactive_limit}
KillWait={kill_wait}
MinJobAge={min_job_age}
SlurmctldTimeout={slurmctld_timeout}
SlurmdTimeout={slurmd_timeout}
Waittime={wait_time}
SchedulerType={scheduler_type}
SelectType={select_type}
SelectTypeParameters={select_type_parameters}
AccountingStorageType={accounting_storage_type}
JobCompType={job_comp_type}
JobAcctGatherFrequency={job_acct_gather_frequency}
JobAcctGatherType={job_acct_gather_type}
SlurmctldDebug={slurmctld_debug}
SlurmctldLogFile={slurmctld_log_file}
SlurmdDebug={slurmd_debug}
SlurmdLogFile={slurmd_log_file}
#
# COMPUTE NODES
NodeName={node_name} CPUs={cpus} RealMemory={real_memory} State={state}
PartitionName={partition_name} Nodes={nodes} Default={default} MaxTime={max_time}
''')

    # Find the destination directory for slurm.conf
    destination_path = find_slurm_directory()
    
    if destination_path:
        # Move slurm.conf to the found directory
        shutil.move('slurm.conf', destination_path)
        print(f"slurm.conf has been moved to {destination_path}")
        
        # Change permissions of the slurm.conf file
        os.chmod(os.path.join(destination_path, 'slurm.conf'), 0o755)
        print("Permissions for slurm.conf have been changed.")
    else:
        print("No slurm configuration directory found in /etc. Manual intervention may be required.")

if __name__ == "__main__":
    install_slurm()
    generate_slurm_conf()
