#!/bin/bash

# example:
# ./create_trajectory_files.sh 0 1.0 2.0 0.0 1.5 2.5 RunA

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
    "$input_file" > "$output_file"

echo "Replacement completed. Output saved to $output_file"