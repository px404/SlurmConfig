# SlurmConfig

SlurmConfig is a comprehensive tool for configuring and managing SLURM (Simple Linux Utility for Resource Management) clusters. SLURM is a highly scalable and robust workload manager for Linux clusters, used widely in high-performance computing (HPC) environments. SlurmConfig provides users with a simplified interface to set up, configure, and manage SLURM clusters effortlessly.

With SlurmConfig, users can easily generate SLURM configuration files (`slurm.conf`), automate the installation of SLURM components (`slurmctld` and `slurmd`), and learn to manage SLURM jobs. With SlurmConfig we get:

- Automated installation of SLURM components using package managers (`apt-get` or `yum`) based on the Linux distribution.
- Configuration file generation with user-friendly prompts to set SLURM parameters such as cluster name, node settings, scheduling policies, and more.
- Step-by-step guide and documentation for submitting jobs.
 
## Run Configuration

To configure Slurm, run `config.py`.

## Start Slurm with systemd

```
$ sudo systemctl start slurmctld
$ sudo systemctl start slurmd
```

## Set Machine as Idle

To start queuing up jobs, set the machine as idle:

```
$ sudo scontrol update nodename=localhost state=idle
$ sinfo
```

If successful, you should see:

```
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
LocalQ*      up   infinite      1   idle localhost
```

You now have a queue (or "partition" in Slurm lingo) called LocalQ that you can submit your work to.

## Submit Slurm Job

Follow `example_slurm_script.sh` to create a script. To submit the Slurm job script (e.g., `example_slurm_script.sh`), use:

```
$ sbatch example_slurm_script.sh
```

Upon successful submission of a job, SLURM returns a job identifier, an integer number assigned by SLURM to that job (e.g., jobid=1). You’ll see your job identified by this number. Note: you will need this id for specific actions involving the job such as canceling the job. Your job will run in the current directory from where you submit the `sbatch` command (although you can direct it elsewhere in the script, using a `cd` command). After submitting a Slurm job script, upon completion one should get an output file `slurm-«jobid».out` (this filename can be changed via a `#SBATCH –o` option).

[See `slurm_job_manual.md` for detailed explanation on submitting/performing tasks.]

## Troubleshooting

If you encounter any issues, you can debug them by looking in the logs in `/var/log/slurm/slurmd.log` and `/var/log/slurm/slurmctld.log`.

## Editing Configuration

Now you have a working Slurm queue, if you need to make changes to your configuration, edit the `slurm.conf` file and restart `slurmctld` and `slurmd` via systemd.
