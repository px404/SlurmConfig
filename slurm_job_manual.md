# Slurm Job Manual

## 1. Template

To submit a job, you can use the template `example_slurm_script.sh`. This can be edited - just change the number of cores etc according to your requirements.

## 2. Submit Actual Work

The template is just an example to check if file submissions are working. Here is an example to submit actual jobs.

To specify tasks inside a SLURM batch script, you typically include the commands necessary to execute your task after the SLURM directives. These commands will depend on the specific task you want to run.

For example, if you need to run a machine learning algorithm, you would include the commands to execute the algorithm after the SLURM directives in your script. Here's an example of how you might structure your SLURM script to run a Python script that trains a machine learning model:

```bash
#!/bin/bash
#
# Example SLURM script to run a machine learning task on the LocalQ queue.

# Set name of submitted job
#SBATCH -J ml_job

# Ask for 3 cores
#SBATCH -n 3

# Submit with maximum 24 hour walltime HH:MM:SS
#SBATCH -t 24:00:00

# Load necessary modules (if required)
# module load python/3.8

# Change directory to where your Python script is located
cd /path/to/your/python/script/directory

# Activate virtual environment (if required)
# source /path/to/your/virtual/env/bin/activate

# Run your Python script that trains the ML model
python train_model.py
```

In this example:

- SLURM directives (`#SBATCH`) are used to specify job parameters such as job name (`-J`), number of cores (`-n`), and maximum walltime (`-t`).
- Optional steps may include loading necessary modules (`module load`) or activating a virtual environment (`source activate`).
- The script changes directory to where your Python script is located using `cd`.
- Finally, the Python script (`train_model.py`) is executed using the `python` command.

## 3. Submit the job

Ok so the setup is done, everything is ready, but how do we submit it for it to be worked upon?

Follow `example_slurm_script.sh` to create a script.

To submit the Slurm job script (e.g., `example_slurm_script.sh`), use:

```bash
$ sbatch example_slurm_script.sh

Submitted batch job 1
```

Upon successful submission of a job, SLURM returns a job identifier, an integer number assigned by SLURM to that job (here, `jobid=1`).

You’ll see your job identified by this number.

> Note: you will need this id for specific actions involving the job such as canceling the job.

Your job will run in the current directory from where you submit the `sbatch` command (although you can direct it elsewhere in the script, using a `cd` command). After submitting a SLURM job script, upon completion one should get an output file `slurm-«jobid».out` (this filename can be changed via a `#SBATCH –o` option).

[See `slurm_job_manual.md` for detailed explanation on submitting/performing tasks.]

If you have any issues you can debug it by looking in the logs in `/var/log/slurm/slurmd.log` and `/var/log/slurm/slurmctld.log` (The path is relative).

If you need to make changes to your config edit the `slurm.conf` and restart `slurmctld` and `slurmd` via systemd for the changes.
