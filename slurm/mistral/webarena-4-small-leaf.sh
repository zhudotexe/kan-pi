#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=rd-wa-small-leaf
#
#SBATCH --output=/nlpgpu/data/andrz/logs/%j.%x.log
#SBATCH --error=/nlpgpu/data/andrz/logs/%j.%x.log
#SBATCH --time=7-0
#SBATCH --nodes=1
#SBATCH -c 16
#SBATCH --mem=400G
#SBATCH --gpus=8
#SBATCH --constraint=48GBgpu
#SBATCH --mail-user=andrz@seas.upenn.edu
#SBATCH --mail-type=END,FAIL

source slurm/env.sh
source slurm/webarena-env.sh
srun python bench_webarena.py --config small-leaf --large-model mistralai/Mistral-Large-Instruct-2407 --small-model mistralai/Mistral-Small-Instruct-2409 --save-dir /nlpgpu/data/andrz/redel/experiments/webarena/test/small-leaf
