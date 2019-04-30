#!/bin/bash
#SBATCH -n 1
#SBATCH -p gpu
#SBATCH -t 00:30:00
#SBATCH --mem=10000
#SBATCH -J gpu_job
#SBATCH -o gpu_job.out.%j
#SBATCH -e gpu_job.err.%j
#SBATCH --gres=gpu:k80:1
#SBATCH                                                                                                                
ONMTTEST=~/OpenNMT-py/translate.py
                                           
module purge
module load python-env/intelpython3.6-2018.3 gcc/5.4.0 cuda/9.0 cudnn/7.1-cuda9

LAN=SOMELAN

echo $LAN
python $ONMTTEST -model models/$LAN-model_step_10000.pt -src opennmtdata/$LAN-src-test.txt -output results/$LAN-src-test.txt.out -replace_unk -verbose  -gpu 0 -n_best 10 -beam 10 > results/$LAN-src-test.txt.nbest.out

