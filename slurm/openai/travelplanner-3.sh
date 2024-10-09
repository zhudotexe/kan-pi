#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=rd-tp-3
#
#SBATCH --output=/nlpgpu/data/andrz/logs/%j.%x.log
#SBATCH --error=/nlpgpu/data/andrz/logs/%j.%x.log
#SBATCH --time=7-0
#SBATCH -c 1
#SBATCH --mem=128G
#SBATCH --mail-user=andrz@seas.upenn.edu
#SBATCH --mail-type=END,FAIL

source slurm/env.sh
srun python bench_travelplanner.py --config full --large-model gpt-4o-2024-05-13 --small-model gpt-3.5-turbo-0125 --save-dir /nlpgpu/data/andrz/redel/experiments/travelplanner/validation/full
srun python bench_travelplanner.py --config root-fc --large-model gpt-4o-2024-05-13 --small-model gpt-3.5-turbo-0125 --save-dir /nlpgpu/data/andrz/redel/experiments/travelplanner/validation/root-fc
srun python bench_travelplanner.py --config baseline --large-model gpt-4o-2024-05-13 --small-model gpt-3.5-turbo-0125 --save-dir /nlpgpu/data/andrz/redel/experiments/travelplanner/validation/baseline
