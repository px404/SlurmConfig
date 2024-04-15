# SlurmConfig

> Run config.py

> Start slurm with systemd:

$ sudo systemctl start slurmctld

$ sudo systemctl start slurmd

> Set machine as idle - to start queuing up jobs
$ sudo scontrol update nodename=localhost state=idle

$ sinfo

If successful you see:

PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST

LocalQ*      up   infinite      1   idle localhost

> You now have a queue(or “partition” in slurm lingo) called LocalQ that you can now submit your work to.

## Submit Slurm Job
> Follow example_slurm_script.sh to create a script

> To submit the slurm job script (here: example_slurm_script.sh) use: $ sbatch example_slurm_script.sh

> Submitted batch job 1

Upon successful submission of a job, SLURM returns a job identifier, an integer number assigned by SLURM to that job (here, jobid=1). You’ll see your job identified by this number
Note: you will need this id for specific actions involving the job such as canceling the job.
Your job will run in the current directory from where you submit the sbatch command (although you can direct it elsewhere in the script, using a cd command). After submitting a slurm job script, upon completion one should get an output file slurm-«jobid».out (this filename can be changed via a #SBATCH –o option).

[See job_manual for detailed explanation on submitting/performing tasks.]

If you have any issues you can debug it by looking in the logs in /var/log/slurm/slurmd.log and /var/log/slurm/slurmctld.log [The path is relative]

Now you have a working slurm queue, if you need to make changes to your config edit the slurm.conf and restart slurmctld and slurmd via systemd.
