#!/bin/bash

# the original trajectory for Lilleengen+ (2023) models
# ./create_trajectory_files.sh 0.16 2.15 -.12 -0.02 -0.85 -0.25 RunA

# something like the original trajectories but not
# ./create_trajectory_files.sh 0.16 2.15 0.5 -0.02 -0.85 -0.35 RunD

# a simple rewind trajectory
# ./create_trajectory_files.sh 0.247 2.53 0.238 -0.011 -0.597 -0.355 RunH

# and some perturbations
# ./create_trajectory_files.sh 0.247 2.63 0.238 -0.011 -0.597 -0.355 RunI

# ./create_trajectory_files.sh 0.247 2.53 0.338 -0.011 -0.597 -0.355 RunJ
# ./create_trajectory_files.sh 0.247 2.53 0.138 -0.011 -0.597 -0.355 RunK
# ./create_trajectory_files.sh 0.247 2.43 0.238 -0.011 -0.597 -0.355 RunL
# ./create_trajectory_files.sh 0.247 2.53 0.238 -0.011 -0.597 -0.455 RunM

# ./create_trajectory_files.sh 0.197 2.53 0.238 -0.011 -0.597 -0.355 RunN
# ./create_trajectory_files.sh 0.297 2.53 0.238 -0.011 -0.597 -0.355 RunO
# ./create_trajectory_files.sh 0.247 2.53 0.238 -0.051 -0.597 -0.355 RunP
# ./create_trajectory_files.sh 0.247 2.43 0.238 -0.011 -0.597 -0.355 RunQ

# ./create_trajectory_files.sh 0.247 2.53 0.238 -0.011 -0.597 -0.405 RunR
# ./create_trajectory_files.sh 0.147 2.53 0.238 -0.011 -0.597 -0.455 RunS
# ./create_trajectory_files.sh 0.197 2.53 0.238 -0.011 -0.597 -0.455 RunT
# ./create_trajectory_files.sh 0.197 2.53 0.238 -0.011 -0.597 -0.405 RunU

# re-run RunH??
# ./create_trajectory_files.sh 0.247 2.53 0.238 -0.011 -0.597 -0.355 RunV

# force scaling to try and match Sophia's targets
# ./create_trajectory_files.sh 0.41 2.31 -0.52 -0.12 -1.04 -0.11 RunW
# ./create_trajectory_files.sh 0.41 2.31 -0.42 -0.12 -1.04 -0.11 RunX
# ./create_trajectory_files.sh 0.41 2.31 -0.62 -0.12 -1.04 -0.11 RunY # this is the current default run

# ./create_trajectory_files.sh 0.41 2.31 -0.62 -0.14 -1.25 -0.13 RunZ
# ./create_trajectory_files.sh 0.41 2.31 -0.62 -0.10 -0.80 -0.09 RunB
# ./create_trajectory_files.sh 0.41 2.31 -0.67 -0.12 -1.04 -0.11 RunC
# ./create_trajectory_files.sh 0.41 2.31 -0.72 -0.12 -1.04 -0.11 RunD

# trying a warping test
# ./create_trajectory_files.sh 0.45 2.22 -0.98 -0.15 -1.04 0.04 RunE
# ./create_trajectory_files.sh 0.52 2.77 -1.14 -0.20 -1.41 0.22 RunF
# ./create_trajectory_files.sh 0.63 3.23 -1.62 -0.28 -1.78 0.55 RunG

# to be run...
# ./create_trajectory_files.sh 0.68 3.12 -1.97 -0.31 -1.78 0.70 RunGA
# ./create_trajectory_files.sh 0.68 3.12 -1.62 -0.31 -1.78 0.55 RunGB
# ./create_trajectory_files.sh 0.66 3.49 -1.70 -0.31 -1.95 0.61 RunGC
# ./create_trajectory_files.sh 0.60 2.97 -1.78 -0.34 -1.61 0.67 RunGD


# Check if the correct number of arguments is provided
if [ "$#" -ne 7 ]; then
    echo "Usage: $0 X Y Z U V W Name"
    exit 1
fi

# Define the variables to be replaced
X="$1"
Y="$2"
Z="$3"
U="$4"
V="$5"
W="$6"
NAME="$7"

# Make a python script that will offset the LMC
input_file="move_lmc_template.py"
output_file="move_lmc_${NAME}.py"

# Replace variables in the input file and save the result to the output file
sed -e "s/{{OFFSETX}}/$X/g" \
    -e "s/{{OFFSETY}}/$Y/g" \
    -e "s/{{OFFSETZ}}/$Z/g" \
    -e "s/{{OFFSETU}}/$U/g" \
    -e "s/{{OFFSETV}}/$V/g" \
    -e "s/{{OFFSETW}}/$W/g" \
    -e "s/{{NAME}}/$NAME/g" \
    "$input_file" > "$output_file"

# run the file
python $output_file


# Specify the input file and output file for the EXP input
input_file="run_template_gpu.yml"
output_file="run_gpu_${NAME}"

# Replace variables in the input file and save the result to the output file
sed -e "s/{{OFFSETX}}/$X/g" \
    -e "s/{{OFFSETY}}/$Y/g" \
    -e "s/{{OFFSETZ}}/$Z/g" \
    -e "s/{{OFFSETU}}/$U/g" \
    -e "s/{{OFFSETV}}/$V/g" \
    -e "s/{{OFFSETW}}/$W/g" \
    -e "s/{{NAME}}/$NAME/g" \
    "$input_file" > "$output_file"

echo "Replacement completed. Output saved to $output_file"
