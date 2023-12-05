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